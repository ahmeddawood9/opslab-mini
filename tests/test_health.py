from app.api.health import live
from app.main import get_version


def test_liveness_endpoint():
    assert live() == {"status": "live"}


def test_version_endpoint():
    payload = get_version()

    assert payload["app_name"] == "opslab-mini"
    assert payload["version"]
    assert payload["environment"]
    assert payload["timestamp"]
