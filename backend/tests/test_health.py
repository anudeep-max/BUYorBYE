import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

# Keep checks independent of any developer's local .env configuration.
with patch.dict(
    os.environ,
    {"CORS_ORIGINS": " http://localhost:5173 , http://127.0.0.1:5173 "},
):
    from app.main import app


class HealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_health(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_allowed_frontend_origins(self) -> None:
        for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
            with self.subTest(origin=origin):
                response = self.client.get("/health", headers={"Origin": origin})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.headers["access-control-allow-origin"], origin
                )
                self.assertNotIn("access-control-allow-credentials", response.headers)

    def test_unknown_origin_has_no_cors_permission(self) -> None:
        response = self.client.get(
            "/health", headers={"Origin": "https://untrusted.example"}
        )

        self.assertNotIn("access-control-allow-origin", response.headers)

    def test_allowed_preflight(self) -> None:
        response = self.client.options(
            "/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["access-control-allow-origin"], "http://localhost:5173"
        )
        self.assertEqual(response.headers["access-control-allow-methods"], "GET")

    def test_unknown_origin_preflight_is_rejected(self) -> None:
        response = self.client.options(
            "/health",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "GET",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access-control-allow-origin", response.headers)


if __name__ == "__main__":
    unittest.main()
