import json

from django.test import TestCase, Client
from django.db import IntegrityError
from django.urls import reverse

from .models import AuthUser, OneTimePassword
from .utils import issue_otp


# ------------------------------------------------------------------------
# Phase 2 — AuthUser model + health/db-test endpoints
# ------------------------------------------------------------------------

class AuthUserModelTests(TestCase):
    def test_create_authuser(self):
        user = AuthUser.objects.create(email="Test@Example.com")
        self.assertEqual(user.email, "test@example.com")  # normalized
        self.assertFalse(user.is_verified)

    def test_email_uniqueness(self):
        AuthUser.objects.create(email="dup@example.com")
        with self.assertRaises(IntegrityError):
            AuthUser.objects.create(email="dup@example.com")


class EndpointTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint(self):
        response = self.client.get(reverse("health-check"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_database_test_endpoint(self):
        response = self.client.get(reverse("database-test"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["database"], "connected")


# ------------------------------------------------------------------------
# Phase 3 — OTP send / verify / resend flow
# ------------------------------------------------------------------------

class OTPFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "otp-test@example.com"

    def test_send_otp_creates_record(self):
        response = self.client.post(
            reverse("otp-send"),
            data=json.dumps({"email": self.email}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(OneTimePassword.objects.filter(email=self.email).exists())

    def test_verify_correct_otp_succeeds(self):
        raw_otp, record = issue_otp(self.email)
        response = self.client.post(
            reverse("otp-verify"),
            data=json.dumps({"email": self.email, "otp": raw_otp}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        record.refresh_from_db()
        self.assertTrue(record.is_verified)

    def test_verify_wrong_otp_increments_attempts(self):
        issue_otp(self.email)
        response = self.client.post(
            reverse("otp-verify"),
            data=json.dumps({"email": self.email, "otp": "000000"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        record = OneTimePassword.objects.filter(email=self.email).first()
        self.assertEqual(record.attempts, 1)

    def test_resend_blocked_by_cooldown(self):
        issue_otp(self.email)
        response = self.client.post(
            reverse("otp-resend"),
            data=json.dumps({"email": self.email}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 429)