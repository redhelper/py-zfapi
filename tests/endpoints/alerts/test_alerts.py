from pytest_httpx import HTTPXMock

from client import ZFApi


class TestAlertsEndpoint:
    """
    Tests for the /1.1/alerts/ endpoint
    """

    zfapi = ZFApi("some_token", "test")

    def test_get_200(self, httpx_mock: HTTPXMock, get_response_obj):
        """
        Hits the /1.1/alerts/{alert_id} endpoint
        using the correct attributes
        """
        # setup mock response
        expected_response = get_response_obj(
            "tests/endpoints/alerts/fixtures/get_v1_200.json",
        )
        httpx_mock.add_response(status_code=200, json=expected_response)

        # make the call
        status_code, alert = self.zfapi.alerts.get(
            alert_id=39229922,
        )

        # Check the request params
        mock_request = httpx_mock.get_request()

        assert mock_request is not None
        assert mock_request.method == "GET"
        assert mock_request.url == ("https://api-test.zerofox.com/1.1/alerts/39229922")
        assert mock_request.headers == {
            "host": "api-test.zerofox.com",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "user-agent": "python-httpx/0.26.0",
            "authorization": "Token some_token",
            "content-type": "application/json",
        }

        # Check the response
        assert status_code == 200
        assert alert == expected_response

    def test_simple_list_200(self, httpx_mock: HTTPXMock, get_response_obj):
        """
        Hits the /1.1/alerts/{query_params} endpoint
        using the correct attributes
        """
        # setup mock response
        expected_response = get_response_obj(
            "tests/endpoints/alerts/fixtures/list_v1_200.json",
        )
        httpx_mock.add_response(status_code=200, json=expected_response)

        # make the call
        status_code, alerts, pagination = self.zfapi.alerts.simple_list(
            query_params={
                "enterprise_id": 2831,
                "limit": 2,
            },
        )

        # Check the request params
        mock_request = httpx_mock.get_request()

        assert mock_request is not None
        assert mock_request.method == "GET"
        assert mock_request.url == (
            "https://api-test.zerofox.com/1.1/alerts/?enterprise_id=2831&limit=2"
        )
        assert mock_request.headers == {
            "host": "api-test.zerofox.com",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "user-agent": "python-httpx/0.26.0",
            "authorization": "Token some_token",
            "content-type": "application/json",
        }

        # Check the response
        assert status_code == 200
        assert alerts == expected_response["alerts"]

        expected_response.pop("alerts")
        assert pagination == expected_response
