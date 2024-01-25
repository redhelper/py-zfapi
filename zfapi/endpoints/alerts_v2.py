import logging

from zfapi.endpoints.alerts import Alerts
from zfapi.endpoints.base import versionT

logger = logging.getLogger(__name__)


class AlertsV2(Alerts):
    """
    Methods to hit the /2.0/alerts/ endpoint on version 2.0
    """

    endpoint: str = "alerts"
    version: versionT = "2.0"

    # everything is already implemented on alerts V1 lol
