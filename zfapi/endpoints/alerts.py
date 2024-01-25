import logging
from typing import Any

from zfapi.endpoints.base import BaseEndpoint, versionT
from zfapi.exceptions import PyZFApiException

logger = logging.getLogger(__name__)


class Alerts(BaseEndpoint):
    """
    Methods to hit the /1.1/alerts/ endpoint on version 1.1
    """

    endpoint: str = "alerts"
    version: versionT = "1.1"

    def get(self, alert_id: int):
        """
        Hits the /1.1/alerts/{alert_id}/ endpoint
        """
        # Validation
        if not isinstance(alert_id, int) or not alert_id:
            raise PyZFApiException(
                f"Received invalid parameter [{alert_id=}]",
            )

        # GET call
        return super().get(get_id=alert_id)

    def simple_list(
        self,
        query_params: dict[str, Any] = {},
    ) -> tuple[int, list[dict[str, str]], dict[str, str]]:
        """
        Hits the /1.1/alerts/{query_params} endpoint
        """
        # LIST call
        return super().simple_list(
            query_params=query_params,
            results_key="alerts",
        )
