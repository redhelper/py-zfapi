from typing import Any

from zfapi.endpoints.base import BaseEndpoint, versionT
from zfapi.exceptions import PyZFApiException


class Entities(BaseEndpoint):
    """
    Methods to hit the /1.1/entities/ endpoint
    """

    endpoint = "entities"
    version: versionT = "1.1"

    def get(self, entity_id: int):
        """
        Hits the /1.1/entities/{entity_id}/ endpoint
        """
        # Validation
        if not isinstance(entity_id, int) or not entity_id:
            raise PyZFApiException(
                f"Received invalid parameter [{entity_id=}]",
            )

        # GET call
        return super().get(get_id=entity_id)

    def simple_list(self, query_params: dict[str, Any] = {}):
        """
        Hits the /1.1/entities/{query_params} endpoint
        """
        # LIST call
        return super().simple_list(
            query_params=query_params,
            results_key="entities",
        )
