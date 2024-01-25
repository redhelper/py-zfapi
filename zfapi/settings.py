import os

# Retry logic
ZFAPI_RETRIES = int(os.environ.get("ZFAPI_RETRIES", 5))

# - Seconds between retries (multiplied with # of attempts)
ZFAPI_RETRY_SLEEP_STEP_SEC = int(os.environ.get("ZFAPI_RETRY_SLEEP_STEP_SEC", 3))

# Behavior
ZFAPI_RAISE_4XX_ERRORS = bool(int(os.environ.get("ZFAPI_RAISE_4XX_ERRORS", False)))
ZFAPI_RETRY_5XX_ERRORS = bool(int(os.environ.get("ZFAPI_RETRY_5XX_ERRORS", True)))
ZFAPI_TIMEOUT_SECS = int(os.environ.get("ZFAPI_TIMEOUT_SECS", 60))

# Validation
ZFAPI_SUPPORTED_METHODS = {"DELETE", "GET", "PATCH", "POST", "PUT"}
