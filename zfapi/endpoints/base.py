import logging
from time import sleep
from typing import Any, Iterable, Literal, Optional
from urllib.parse import parse_qs, urlparse

import httpx

from zfapi.exceptions import PyZFApiException, ZFApiHttpException
from zfapi.settings import (
    ZFAPI_RAISE_4XX_ERRORS,
    ZFAPI_RETRIES,
    ZFAPI_RETRY_5XX_ERRORS,
    ZFAPI_RETRY_SLEEP_STEP_SEC,
    ZFAPI_SUPPORTED_METHODS,
)

logger = logging.getLogger(__name__)

versionT = Literal["1.0", "1.1", "2.0"]


class BaseEndpoint:
    """
    This class represents a wrapper for interactions
    with a given ZeroFOX API endpoint
    """

    # Set these on each new endpoint
    endpoint: str = ""
    version: versionT = "1.0"

    def __init__(self, session: httpx.Client) -> None:
        """
        Initializes a wrapper to make requests to
        a particular endpoint in the ZeroFox API.
        """
        self._session = session

    ############################################################################
    # Validation Helpers
    ############################################################################
    @staticmethod
    def is_2XX_status_code(status_code: int) -> bool:
        return 200 <= status_code < 300

    @staticmethod
    def is_4XX_status_code(status_code: int) -> bool:
        return 400 <= status_code < 500

    @staticmethod
    def is_5XX_status_code(status_code: int) -> bool:
        return 500 <= status_code < 600

    ############################################################################
    # Request Makers
    ############################################################################
    def make_request(
        self,
        method="GET",
        version: versionT = "1.0",
        endpoint: Optional[str] = None,
        pk: int = 0,
        params: dict = {},
    ) -> tuple[int, dict]:
        """
        Executes the calls to ZFAPI using self.session
        By default it stops on 4XX errors and retries 5XXs
        """
        # fail on unsupported methods
        if method not in ZFAPI_SUPPORTED_METHODS:
            raise PyZFApiException(f"Got unsupported method [{method=}]")

        # fail when there's no endpoint defined
        if not endpoint:
            raise PyZFApiException("No zfapi endpoint was provided")

        # cast pk to str if any
        pk_str = f"{pk}" if pk else ""

        url = f"/{version}/{endpoint}/{pk_str}"

        # empty response
        resp = httpx.Response(status_code=0, json={"error": "request was not sent"})

        for retry_count in range(ZFAPI_RETRIES):
            try:
                resp = self._session.request(
                    method=method,
                    url=url,
                    params=params,
                )

                # handle 4XX errors
                if self.is_4XX_status_code(resp.status_code):
                    # raise if enabled
                    if ZFAPI_RAISE_4XX_ERRORS:
                        raise ZFApiHttpException(
                            "Got unexpected ZF-API response "
                            f"[{resp.status_code=}, {url=!s}, "
                            f"{params=}, {resp.text=}]"
                        )

                # handle 5XX errors
                elif self.is_5XX_status_code(resp.status_code):
                    # retry if enabled
                    if ZFAPI_RETRY_5XX_ERRORS:
                        logger.warning(
                            "Retrying 5XX ZF-API response "
                            "[url=%s, resp.status_code=%d, retries=%d]",
                            url,
                            resp.status_code,
                            retry_count + 1,
                        )
                        # wait some secs before trying again
                        sleep((retry_count + 1) * ZFAPI_RETRY_SLEEP_STEP_SEC)
                        continue

                # return if there's no unexpected errors
                break

            except ZFApiHttpException:
                raise

            # Catch HTTP errors
            except Exception as e:
                if (retry_count) < ZFAPI_RETRIES:
                    logger.warning(
                        "pyZF-API Retrying failed request [url=%s, error=%s, retries=%d]",
                        url,
                        str(e),
                        retry_count + 1,
                    )
                    sleep((retry_count + 1) * ZFAPI_RETRY_SLEEP_STEP_SEC)

                else:
                    logger.error("pyZF-API request failed [url=%s, error=%s]", url, e)
                    raise ZFApiHttpException(e)

        if resp.status_code == 0:
            ZFApiHttpException("pyZF-API fatal error: could not get a valid response")

        return resp.status_code, resp.json()

    def paginated_requests(
        self,
        request_function,
        query_params: dict[str, Any] = {},
        pages: int = -1,
    ) -> Iterable[tuple[int, list[dict[str, str]], dict[str, str]]]:
        """
        Helper function to hit endpoints with support for looping the results
        """
        initial_pages = pages
        more_pages = True

        while more_pages and pages != 0:
            status_code, results, pagination = request_function(query_params)
            yield status_code, results, pagination

            if "next" in pagination and pagination["next"] is not None:
                next_page = urlparse(pagination["next"])
                query_params = parse_qs(next_page.query)
            else:
                more_pages = False

            pages -= 1

        if pages == 0:
            logger.debug("pyZF-API: Reached limit of pages [pages=%s]", initial_pages)
        else:
            logger.debug("pyZF-API: Got all available results")

    ############################################################################
    # Endpoint Calls
    ############################################################################
    def get(self, get_id: int):
        """
        Hits the /{self.version}/{self.endpoint}/{get_id}/ endpoint
        """
        return self.make_request(
            version=self.version,
            endpoint=self.endpoint,
            pk=get_id,
        )

    def simple_list(
        self,
        query_params: dict[str, Any] = {},
        results_key="results",
    ) -> tuple[int, list[dict[str, str]], dict[str, str]]:
        """
        Hits the /{self.version}/{self.endpoint}/{query_params} endpoint
        """
        status_code, response_json = self.make_request(
            version=self.version,
            endpoint=self.endpoint,
            params=query_params,
        )

        results = []
        if BaseEndpoint.is_2XX_status_code(status_code):
            results = response_json.pop(results_key)

        return status_code, results, response_json

    def iterable_list(
        self,
        query_params: dict[str, Any] = {},
        pages: int = -1,
    ) -> Iterable[tuple[int, list[dict[str, str]], dict[str, str]]]:
        """
        Hits the /{self.version}/{self.endpoint}/{query_params} endpoint
        with support for looping the function results
        """
        yield from self.paginated_requests(
            request_function=self.simple_list,
            query_params=query_params,
            pages=pages,
        )
