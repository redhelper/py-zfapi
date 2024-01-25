from typing import Any

from zfapi.endpoints.base import BaseEndpoint, versionT
from zfapi.exceptions import PyZFApiException


class Enterprises(BaseEndpoint):
    """
    Methods to hit the /1.0/enterprises/ endpoint
    """

    endpoint: str = "enterprises"
    version: versionT = "1.0"

    def get(self, enterprise_id: int):
        """
        Hits the /1.0/enterprises/{enterprise_id}/ endpoint
        """
        # Validation
        if not isinstance(enterprise_id, int) or not enterprise_id:
            raise PyZFApiException(
                f"Received invalid parameter [{enterprise_id=}]",
            )

        # GET call
        return super().get(get_id=enterprise_id)

    def simple_list(self, query_params: dict[str, Any] = {}):
        """
        Hits the /1.0/enterprises/{query_params} endpoint

        WARNING: This endpoint has no pagination. It will return all enterprises
        on a single page.
        """
        # LIST call
        return super().simple_list(
            query_params=query_params,
            results_key="enterprises",
        )
