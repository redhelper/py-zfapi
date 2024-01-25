import httpx
import pytest
from pytest_httpx import HTTPXMock

from zfapi.endpoints.base import BaseEndpoint
from zfapi.exceptions import PyZFApiException, ZFApiHttpException


class TestBaseEndpoint:
    def test_endpoint_init(self):
        """
        All endpoints should set session when created
        """
        client = httpx.Client()
        endpoint = BaseEndpoint(client)

        assert endpoint._session == client

    @pytest.mark.parametrize(
        ("status_code", "result"),
        (
            pytest.param(0, False),
            pytest.param(199, False),
            pytest.param(200, True),
            pytest.param(250, True),
            pytest.param(299, True),
            pytest.param(300, False),
        ),
    )
    def test_is_2XX_status_code(self, status_code, result):
        """
        Should recognize 4XX errors properly
        """
        assert BaseEndpoint.is_2XX_status_code(status_code) is result

    @pytest.mark.parametrize(
        ("status_code", "result"),
        (
            pytest.param(0, False),
            pytest.param(399, False),
            pytest.param(400, True),
            pytest.param(450, True),
            pytest.param(499, True),
            pytest.param(500, False),
        ),
    )
    def test_is_4XX_status_code(self, status_code, result):
        """
        Should recognize 4XX errors properly
        """
        assert BaseEndpoint.is_4XX_status_code(status_code) is result

    @pytest.mark.parametrize(
        ("status_code", "result"),
        (
            pytest.param(0, False),
            pytest.param(499, False),
            pytest.param(500, True),
            pytest.param(550, True),
            pytest.param(599, True),
            pytest.param(600, False),
        ),
    )
    def test_is_5XX_status_code(self, status_code, result):
        """
        Should recognize 5XX errors properly
        """
        assert BaseEndpoint.is_5XX_status_code(status_code) is result

    def test_make_request_happy_path(self, httpx_mock: HTTPXMock):
        """
        Should handle requests to any specified url:
        - Builds the proper url format
        - Includes method, version and params
        - Returns status code and JSON response

        """
        sample_response = {"result": "all good!"}
        httpx_mock.add_response(status_code=200, json=sample_response)

        with httpx.Client(
            base_url="https://api-mock.zerofox.com",
        ) as client:
            endpoint = BaseEndpoint(client)
            (
                status_code,
                response_json,
            ) = endpoint.make_request(
                method="GET",
                version="1.1",
                endpoint="peepeepoopoo",
                pk=1234,
                params={
                    "hello": "goodbye",
                },
            )

        # Check the request
        mock_request = httpx_mock.get_request()
        assert mock_request is not None
        assert mock_request.method == "GET"
        assert mock_request.url == (
            "https://api-mock.zerofox.com/1.1/peepeepoopoo/1234?hello=goodbye"
        )

        # Check the response
        assert status_code == 200
        assert response_json == sample_response

    @pytest.mark.parametrize(
        (
            "method",
            "endpoint",
            "status_code",
            "expected_exc",
        ),
        (
            pytest.param(
                "OPTIONS",
                "",
                0,
                PyZFApiException("Got unsupported method [method='OPTIONS']"),
                id="method='OPTIONS'",
            ),
            pytest.param(
                "HEAD",
                "",
                0,
                PyZFApiException("Got unsupported method [method='HEAD']"),
                id="method='HEAD'",
            ),
            pytest.param(
                "POST",
                "",
                0,
                PyZFApiException("No zfapi endpoint was provided"),
                id="empty_endpoint",
            ),
            pytest.param(
                "POST",
                "somewhere",
                418,
                ZFApiHttpException(
                    "Got unexpected ZF-API response ["
                    "resp.status_code=418, "
                    "url=/1.0/somewhere/1234, "
                    "params={'hello': 'goodbye'}, "
                    """resp.text=\'{"error": "i\\\'m a toast!"}\']"""
                ),
                id="error_code_418",
            ),
        ),
    )
    def test_make_request_raises_unsupported_method(
        self,
        httpx_mock: HTTPXMock,
        mocker,
        method,
        endpoint,
        status_code,
        expected_exc,
    ):
        """
        Should error out if:
        - Requests an unsupported method
        - There's no endpoint defined
        - Gets a 4XX error with raise setting enabled
        """
        # setup env var and response if a status_code is passed
        if status_code:
            mocker.patch(
                "zfapi.endpoints.base.ZFAPI_RAISE_4XX_ERRORS",
                True,
            )
            mocker.patch(
                "zfapi.endpoints.base.ZFAPI_RETRIES",
                1,
            )

            sample_response = {"error": "i'm a toast!"}
            httpx_mock.add_response(
                status_code=status_code,
                json=sample_response,
            )

        exc_type = type(expected_exc)

        with httpx.Client(
            base_url="https://api-mock.zerofox.com",
        ) as client:
            base_endpoint = BaseEndpoint(client)

            with pytest.raises(exc_type) as exception:
                base_endpoint.make_request(
                    method=method,
                    version="1.0",
                    endpoint=endpoint,
                    pk=1234,
                    params={
                        "hello": "goodbye",
                    },
                )

        # Check the error raised
        assert exception.errisinstance(exc_type) is True
        assert str(exception.value) == str(expected_exc)
