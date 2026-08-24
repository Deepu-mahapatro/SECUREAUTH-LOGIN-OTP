import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_verification_email(email: str, otp: str, expiry_minutes: int) -> bool:
    """
    Sends the OTP to the user's inbox.

    Returns True on success, False on failure — never raises, so the
    caller decides what to do (see utils.py: a failed send means the
    OTP record must NOT be created/kept).
    """
    subject = "Your SecureAuth verification code"
    message = (
        "Hello,\n\n"
        "Your SecureAuth verification code is:\n\n"
        f"{otp}\n\n"
        f"This code expires in {expiry_minutes} minutes.\n\n"
        "If you did not request this code, you can safely ignore this email.\n"
        "Do not share this code with anyone.\n\n"
        "Regards,\nSecureAuth"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception:
        # Log that sending failed — but NEVER log the OTP itself or any
        # SMTP credential. logger.exception() captures the traceback for
        # your own debugging without printing secrets.
        logger.exception("Failed to send verification email to %s", email)
        return False