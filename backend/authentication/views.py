from django.shortcuts import render
import json
import re
import dns.resolver

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AuthUser, OneTimePassword
from .utils import (
    issue_otp,
    get_latest_otp,
    seconds_since_last_sent,
    OTPDeliveryError,
)


# ------------------------------------------------------------------------
# HTML Pages
# ------------------------------------------------------------------------

def home(request):
    return render(request, "index.html")


def verify_page(request):
    return render(request, "verify.html")


def success_page(request):
    return render(request, "success.html")


# ------------------------------------------------------------------------
# Health Check + Database Connection Test
# ------------------------------------------------------------------------

def health_check(request):
    """
    GET /api/health/

    Confirms that the Django server is running.
    """
    return JsonResponse({
        "status": "ok",
        "message": "Backend is running",
    })


def database_test(request):
    """
    GET /api/auth/test/

    Confirms that Django can communicate with PostgreSQL
    by executing a real database query.
    """
    try:
        record_count = AuthUser.objects.count()

        return JsonResponse({
            "status": "ok",
            "database": "connected",
            "authuser_records": record_count,
        })

    except DatabaseError:
        return JsonResponse(
            {
                "status": "error",
                "database": "unreachable",
            },
            status=503,
        )

    except Exception:
        return JsonResponse(
            {
                "status": "error",
                "message": "Unexpected server error",
            },
            status=500,
        )


# ------------------------------------------------------------------------
# Email Validation
# ------------------------------------------------------------------------

GMAIL_REGEX = re.compile(
    r"^[^\s@]+@gmail\.com$",
    re.IGNORECASE,
)


def _has_mx_record(email):
    """
    Check whether the email domain has an MX record.

    This confirms that the domain is configured to receive email.
    It does NOT prove that the specific mailbox exists.
    """

    domain = email.rsplit("@", 1)[1].lower()

    try:
        answers = dns.resolver.resolve(domain, "MX")
        return bool(answers)

    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
    ):
        return False

    except Exception:
        # A temporary DNS failure should not block a legitimate user.
        return True


def _parse_json_body(request):
    """
    Safely parse JSON request body.

    Returns:
        (data, None) when successful
        (None, JsonResponse) when invalid
    """

    try:
        data = json.loads(request.body or "{}")

        if not isinstance(data, dict):
            return None, JsonResponse(
                {"error": "Invalid JSON body."},
                status=400,
            )

        return data, None

    except json.JSONDecodeError:
        return None, JsonResponse(
            {"error": "Invalid JSON body."},
            status=400,
        )


def _validate_email_or_error(email):
    """
    Validate the email address.

    Current project allows Gmail addresses only.
    """

    if not email:
        return JsonResponse(
            {
                "error": "Please enter your email address.",
            },
            status=400,
        )

    email = email.strip().lower()

    # 1. Validate email syntax
    try:
        validate_email(email)

    except ValidationError:
        return JsonResponse(
            {
                "error": "Please enter a valid email address.",
            },
            status=400,
        )

    # 2. Gmail only
    if not GMAIL_REGEX.fullmatch(email):
        return JsonResponse(
            {
                "error": "Please enter a valid Gmail address.",
            },
            status=400,
        )

    # 3. Check MX record
    if not _has_mx_record(email):
        return JsonResponse(
            {
                "error": "This email domain cannot receive email.",
            },
            status=400,
        )

    return None


# ------------------------------------------------------------------------
# OTP - SEND
# ------------------------------------------------------------------------

@csrf_exempt
@require_POST
def send_otp(request):
    """
    POST /api/otp/send/

    Expected JSON:
    {
        "email": "user@gmail.com"
    }
    """

    data, error = _parse_json_body(request)

    if error:
        return error

    email = (data.get("email") or "").strip().lower()

    # Validate email
    error = _validate_email_or_error(email)

    if error:
        return error

    # Check OTP cooldown
    existing = get_latest_otp(email)

    if existing:
        elapsed = seconds_since_last_sent(existing)

        if elapsed < settings.OTP_RESEND_COOLDOWN_SECONDS:

            remaining = max(
                1,
                int(
                    settings.OTP_RESEND_COOLDOWN_SECONDS
                    - elapsed
                ),
            )

            return JsonResponse(
                {
                    "error": (
                        f"Please wait {remaining} seconds "
                        "before requesting another code."
                    )
                },
                status=429,
            )

    try:
        # Send OTP first.
        issue_otp(email)

        # Only create the user after OTP delivery succeeds.
        AuthUser.objects.get_or_create(
            email=email,
            defaults={
                "is_verified": False,
            },
        )

    except OTPDeliveryError:
        return JsonResponse(
            {
                "error": (
                    "We couldn't deliver a verification code "
                    "to this email. Please check that the email "
                    "address is correct."
                )
            },
            status=502,
        )

    except DatabaseError:
        return JsonResponse(
            {
                "error": (
                    "Could not process request. "
                    "Please try again."
                )
            },
            status=503,
        )

    except Exception:
        return JsonResponse(
            {
                "error": (
                    "An unexpected error occurred. "
                    "Please try again."
                )
            },
            status=500,
        )

    return JsonResponse(
        {
            "message": "Verification code sent successfully.",
        },
        status=200,
    )


# ------------------------------------------------------------------------
# OTP - VERIFY
# ------------------------------------------------------------------------

@csrf_exempt
@require_POST
def verify_otp(request):
    """
    POST /api/otp/verify/

    Expected JSON:
    {
        "email": "user@gmail.com",
        "otp": "123456"
    }
    """

    data, error = _parse_json_body(request)

    if error:
        return error

    email = (data.get("email") or "").strip().lower()
    otp_input = (data.get("otp") or "").strip()

    # Validate email
    error = _validate_email_or_error(email)

    if error:
        return error

    # Validate OTP
    if not otp_input:
        return JsonResponse(
            {
                "error": "Please enter the complete 6-digit code.",
            },
            status=400,
        )

    if not otp_input.isdigit() or len(otp_input) != 6:
        return JsonResponse(
            {
                "error": "Please enter a valid 6-digit code.",
            },
            status=400,
        )

    # Get latest OTP
    record = get_latest_otp(email)

    if not record or record.is_verified:
        return JsonResponse(
            {
                "error": (
                    "No active verification code found. "
                    "Request a new one."
                )
            },
            status=404,
        )

    # Check expiration
    if record.is_expired():
        return JsonResponse(
            {
                "error": (
                    "Your verification code has expired. "
                    "Please request a new code."
                )
            },
            status=410,
        )

    # Check maximum attempts
    if record.attempts >= settings.OTP_MAX_ATTEMPTS:
        return JsonResponse(
            {
                "error": (
                    "Too many incorrect attempts. "
                    "Please request a new code."
                )
            },
            status=429,
        )

    # Check OTP
    if not record.check_otp(otp_input):

        record.attempts += 1

        record.save(
            update_fields=["attempts"]
        )

        return JsonResponse(
            {
                "error": (
                    "Invalid verification code. "
                    "Please try again."
                )
            },
            status=400,
        )

    # OTP verified successfully
    record.is_verified = True

    record.save(
        update_fields=["is_verified"]
    )

    # Mark user as verified
    AuthUser.objects.filter(
        email=email
    ).update(
        is_verified=True
    )

    return JsonResponse(
        {
            "message": "Email verified successfully.",
        },
        status=200,
    )


# ------------------------------------------------------------------------
# OTP - RESEND
# ------------------------------------------------------------------------

@csrf_exempt
@require_POST
def resend_otp(request):
    """
    POST /api/otp/resend/

    Expected JSON:
    {
        "email": "user@gmail.com"
    }
    """

    data, error = _parse_json_body(request)

    if error:
        return error

    email = (data.get("email") or "").strip().lower()

    # Validate email
    error = _validate_email_or_error(email)

    if error:
        return error

    # Check existing OTP session
    existing = get_latest_otp(email)

    if not existing:
        return JsonResponse(
            {
                "error": (
                    "No verification session found "
                    "for this email."
                )
            },
            status=404,
        )

    # Check resend cooldown
    elapsed = seconds_since_last_sent(existing)

    if elapsed < settings.OTP_RESEND_COOLDOWN_SECONDS:

        remaining = max(
            1,
            int(
                settings.OTP_RESEND_COOLDOWN_SECONDS
                - elapsed
            ),
        )

        return JsonResponse(
            {
                "error": (
                    f"Please wait {remaining} seconds "
                    "before resending."
                )
            },
            status=429,
        )

    try:
        issue_otp(email)

    except OTPDeliveryError:
        return JsonResponse(
            {
                "error": (
                    "We couldn't resend the verification email. "
                    "Please try again."
                )
            },
            status=502,
        )

    except DatabaseError:
        return JsonResponse(
            {
                "error": (
                    "Could not process request. "
                    "Please try again."
                )
            },
            status=503,
        )

    except Exception:
        return JsonResponse(
            {
                "error": (
                    "An unexpected error occurred. "
                    "Please try again."
                )
            },
            status=500,
        )

    return JsonResponse(
        {
            "message": (
                "Verification code resent successfully."
            )
        },
        status=200,
    )