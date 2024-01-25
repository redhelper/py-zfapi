import logging
import os
import sys

log_level = os.environ.get("LOG_LEVEL", "DEBUG")

root = logging.getLogger()
root.setLevel(log_level)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(log_level)
# formatter = logging.Formatter(
#     '%(asctime)s %(process)d %(thread)d %(funcName)s '
#     '%(lineno)d %(levelname)s %(message)s',
# )
formatter = logging.Formatter(
    "[%(levelname)s] %(message)s",
)
handler.setFormatter(formatter)
root.addHandler(handler)
