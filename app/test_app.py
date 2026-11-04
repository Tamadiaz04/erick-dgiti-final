import unittest

from app import response_for


class AppTests(unittest.TestCase):
    def test_health(self):
        status, body = response_for("/health", {})
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_status(self):
        status, body = response_for("/status", {})
        self.assertEqual(status, 200)
        self.assertEqual(body["database_architecture"], "RDS PostgreSQL primary + read replica")

    def test_unknown_path(self):
        status, body = response_for("/unknown", {})
        self.assertEqual(status, 404)
        self.assertEqual(body["status"], "not_found")


if __name__ == "__main__":
    unittest.main()
