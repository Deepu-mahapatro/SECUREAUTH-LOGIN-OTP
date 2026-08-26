import logging
import os

import resend

logger = logging.getLogger(__name__)


def send_verification_email(email: str, otp: str, expiry_minutes: int) -> bool:
    """
    Sends the OTP using the Resend email API.

    Returns True on success and False on failure.
    Never logs the OTP or API key.
    """

    subject = "Your SecureAuth verification code"

    message = (
        "Hello,\n\n"
        "Your SecureAuth verification code is:\n\n"
        f"{otp}\n\n"
        f"This code expires in {expiry_minutes} minutes.\n\n"
        "If you did not request this code, you can safely ignore this email.\n"
        "Do not share this code with anyone.\n\n"
        "Regards,\n"
        "SecureAuth"
    )

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("EMAIL_FROM")

    logger.info("RESEND_API_KEY configured: %s", bool(api_key))
    logger.info("EMAIL_FROM configured: %s", bool(from_email))
    logger.info("EMAIL_FROM value: %s", from_email)

    if not api_key:
        logger.error("RESEND_API_KEY is not configured.")
        return False

    if not from_email:
        logger.error("EMAIL_FROM is not configured.")
        return False

    try:
        resend.api_key = api_key

        resend.Emails.send(
            {
                "from": from_email,
                "to": [email],
                "subject": subject,
                "text": message,
            }
        )

        return True

    except Exception:
        logger.exception(
            "Failed to send verification email to %s",
            email,
        )
        return False