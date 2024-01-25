import json

import pytest


@pytest.fixture
def get_response_obj():
    def _get_response_obj(path):
        with open(path, "r") as f:
            return json.load(f)

    return _get_response_obj
