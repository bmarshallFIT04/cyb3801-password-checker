import unittest
from app import app


class TestInjectionProtection(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post_password(self, payload):
        return self.client.post("/api/check", json={"password": payload})

    def test_valid_normal_password(self):
        res = self.post_password("CorrectHorseBatteryStaple99!")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("SAFE:", data["injection_protection"])

    def test_sql_injection_payloads(self):
        sqli_payloads = [
            "' OR '1'='1",
            "admin' --",
            "password'; DROP TABLE users; --",
            "1' UNION SELECT username, password FROM users--",
        ]
        for payload in sqli_payloads:
            res = self.post_password(payload)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn("SQL Injection", data["injection_protection"])
            self.assertIn("NEUTRALIZED", data["injection_protection"])

    def test_xss_injection_payloads(self):
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
            "<svg onload=alert('hacked')>",
        ]
        for payload in xss_payloads:
            res = self.post_password(payload)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn("Cross-Site Scripting (XSS)", data["injection_protection"])
            self.assertIn("NEUTRALIZED", data["injection_protection"])

    def test_command_injection_payloads(self):
        cmdi_payloads = [
            "password; ls -la",
            "test && whoami",
            "admin | cat /etc/passwd",
            "pass$(rm -rf /tmp/test)",
        ]
        for payload in cmdi_payloads:
            res = self.post_password(payload)
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn("OS Command Injection", data["injection_protection"])
            self.assertIn("NEUTRALIZED", data["injection_protection"])

    def test_large_and_invalid_inputs_blocked(self):
        # 1. Oversized input (> 128 chars)
        res_large = self.post_password("A" * 5000)
        self.assertEqual(res_large.status_code, 400)
        self.assertIn("maximum length", res_large.get_json()["error"])

        # 2. Null byte injection
        res_null = self.post_password("password\x00admin")
        self.assertEqual(res_null.status_code, 400)
        self.assertIn("null bytes", res_null.get_json()["error"])

        # 3. Empty string
        res_empty = self.post_password("")
        self.assertEqual(res_empty.status_code, 400)

        # 4. Non-string JSON payload
        res_type = self.client.post("/api/check", json={"password": ["array", "attack"]})
        self.assertEqual(res_type.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
