from zfapi.endpoints.base import versionT
from zfapi.endpoints.enterprises import Enterprises


class EnterprisesV2(Enterprises):
    """
    Methods to hit the /2.0/enterprises/ endpoint
    """

    endpoint: str = "alerts"
    version: versionT = "2.0"
