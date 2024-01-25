class PyZFApiException(Exception):
    """
    This class represents a package exception.
    Used for errors when setting up the calls.
    """

    pass


class ZFApiHttpException(Exception):
    """
    This class represents a client exception.
    Used for errors received when hitting the API
    """

    pass
