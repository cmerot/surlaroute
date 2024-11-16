import json
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.utils.schemas import Message


def test_test_email(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    with (
        patch("app.utils.send_email", return_value=None),
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        r = client.post(
            "/utils/test-email/?email_to=test@example.com",
            headers=superuser_token_headers,
        )
        assert Message.model_validate_json(json.dumps(r.json()))
        assert r.status_code == 201


def test_health_check(client: TestClient) -> None:
    r = client.get("/utils/health-check")
    result = r.json()
    assert r.status_code == 200
    assert result
