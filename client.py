import logging
from typing import Literal

import httpx

from zfapi.endpoints.alerts import Alerts
from zfapi.endpoints.alerts_v2 import AlertsV2
from zfapi.endpoints.enterprises import Enterprises
from zfapi.endpoints.enterprises_v2 import EnterprisesV2
from zfapi.endpoints.entities import Entities
from zfapi.exceptions import PyZFApiException
from zfapi.settings import ZFAPI_RETRIES, ZFAPI_RETRY_SLEEP_STEP_SEC, ZFAPI_TIMEOUT_SECS

logger = logging.getLogger(__name__)

envT = Literal["test", "qa", "stag", "prod"]


class ZFApi:
    """
    Main class, encapsulating all available endpoints
    """

    def __init__(
        self,
        token: str,
        env: envT = "qa",
    ):
        """
        Initializes a client to make requests to the ZeroFox API.
        """
        self.validate_settings(env, token)

        # set base params
        self.base_url = f"https://api-{env}.zerofox.com"
        self.token = token

        # initialize only when called
        self._headers = None
        self._session = None

        # Available Endpoints
        self._alerts = None
        self._alerts_v2 = None
        self._enterprises = None
        self._enterprises_v2 = None
        self._entities = None

    @staticmethod
    def validate_settings(env: envT, token: str):
        if ZFAPI_RETRIES < 1:
            raise PyZFApiException(
                f"Invalid ZFAPI_RETRIES value was set [{ZFAPI_RETRIES=}]",
            )
        if ZFAPI_TIMEOUT_SECS < 1:
            raise PyZFApiException(
                f"Invalid ZFAPI_TIMEOUT_SECS value was set [{ZFAPI_TIMEOUT_SECS=}]",
            )
        if ZFAPI_RETRY_SLEEP_STEP_SEC < 1:
            raise PyZFApiException(
                "Invalid ZFAPI_RETRY_SLEEP_STEP_SEC value was set "
                f"[{ZFAPI_RETRY_SLEEP_STEP_SEC=}]",
            )

        # check args
        if not env:
            logger.warning("PyZFApi: Missing env. Using QA as default")

        if not isinstance(token, str) or not token:
            raise PyZFApiException("PyZFApi: No valid token was provided")

    ###########################################################################
    # http Headers
    ###########################################################################
    @property
    def headers(self) -> dict[str, str]:
        if self._headers is None:
            self._headers = {
                "Authorization": "Token " + self.token,
                "Content-Type": "application/json",
            }
        return self._headers

    ###########################################################################
    # httpx Client
    ###########################################################################
    @property
    def session(self) -> httpx.Client:
        if self._session is None:
            self._session = httpx.Client(
                base_url=self.base_url,
                proxies=None,
                timeout=ZFAPI_TIMEOUT_SECS,
                follow_redirects=True,
                headers=self.headers,
            )

        return self._session

    ###########################################################################
    # setup endpoints
    ###########################################################################
    @property
    def alerts(self) -> Alerts:
        if self._alerts is None:
            self._alerts = Alerts(self.session)

        return self._alerts

    @property
    def alerts_v2(self) -> AlertsV2:
        if self._alerts_v2 is None:
            self._alerts_v2 = AlertsV2(self.session)

        return self._alerts_v2

    @property
    def enterprises(self) -> Enterprises:
        if self._enterprises is None:
            self._enterprises = Enterprises(self.session)

        return self._enterprises

    @property
    def enterprises_v2(self) -> EnterprisesV2:
        if self._enterprises_v2 is None:
            self._enterprises_v2 = EnterprisesV2(self.session)

        return self._enterprises_v2

    @property
    def entities(self) -> Entities:
        if self._entities is None:
            self._entities = Entities(self.session)

        return self._entities
