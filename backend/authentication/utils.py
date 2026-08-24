import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import OneTimePassword
from .email_service import send_verification_email


class OTPDeliveryError(Exception):
    """Raised when an OTP was generated but the email could not be sent."""
    pass


def generate_numeric_otp(length: int = 6) -> str:
    """
    Cryptographically secure numeric OTP.
    Uses `secrets.choice`, NOT `random.randint` — `random` is predictable
    and unsafe for anything security-sensitive.
    """
    digits = "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))


def issue_otp(email: str) -> tuple[str, OneTimePassword]:
    """
    Generates, emails, and (only on success) stores a new OTP.

    Order: invalidate old OTPs -> generate -> send email -> save hash.
    The email is sent BEFORE the database write: if sending fails, nothing
    is left behind in PostgreSQL — no orphaned OTP record the user can
    never receive or enter.
    """
    email = email.strip().lower()

    # Invalidate any previous unverified OTPs for this email.
    OneTimePassword.objects.filter(email=email, is_verified=False).update(
        expires_at=timezone.now()
    )

    # Generate — exists only in memory at this point.
    raw_otp = generate_numeric_otp(settings.OTP_LENGTH)

    # Send FIRST. If this fails, nothing is written to PostgreSQL.
    sent = send_verification_email(email, raw_otp, settings.OTP_EXPIRY_MINUTES)
    if not sent:
        raise OTPDeliveryError("Failed to send verification email.")

    # Only now do we store the OTP — and only its hash, never the raw code.
    record = OneTimePassword.objects.create(
        email=email,
        otp_hash=OneTimePassword.hash_otp(raw_otp),
        expires_at=timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
        last_sent_at=timezone.now(),
    )

    # raw_otp is not printed, logged, or stored anywhere from here on —
    # it goes out of scope once this function returns.
    return raw_otp, record


def get_latest_otp(email: str):
    email = email.strip().lower()
    return (
        OneTimePassword.objects.filter(email=email)
        .order_by("-created_at")
        .first()
    )


def seconds_since_last_sent(record: OneTimePassword) -> float:
    return (timezone.now() - record.last_sent_at).total_seconds()