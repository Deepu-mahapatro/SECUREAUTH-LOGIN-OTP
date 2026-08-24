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
from .utils import issue_otp, get_latest_otp, seconds_since_last_sent, OTPDeliveryError

def home(request):
    return render(request, "index.html")


def verify_page(request):
    return render(request, "verify.html")


def success_page(request):
    return render(request, "success.html")

# ------------------------------------------------------------------------
# Phase 2 — health check + database connection test
# ------------------------------------------------------------------------

def health_check(request):
    """GET /api/health/ — confirms the Django server is running."""
    return JsonResponse({
        "status": "ok",
        "message": "Backend is running",
    })


def database_test(request):
    """
    GET /api/auth/test/ — confirms Django can actually talk to PostgreSQL,
    not just that the server process is alive.
    """
    try:
        # A cheap real query — forces Django to open a DB connection
        # and execute SQL, rather than just checking settings.
        record_count = AuthUser.objects.count()

        return JsonResponse({
            "status": "ok",
            "database": "connected",
            "authuser_records": record_count,
        })

    except DatabaseError:
        # Never leak raw exception text (could contain host/user/password
        # hints) — return a safe, generic message instead.
        return JsonResponse(
            {"status": "error", "database": "unreachable"},
            status=503,
        )
    except Exception:
        return JsonResponse(
            {"status": "error", "message": "Unexpected server error"},
            status=500,
        )


# ------------------------------------------------------------------------
# Shared helpers
# ------------------------------------------------------------------------
GMAIL_REGEX = re.compile(
    r"^[^\s@]+@gmail\.com$",
    re.IGNORECASE
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
        # DNS timeout or another temporary/inconclusive
        # DNS problem must not block a legitimate user.
        return True
    
def _parse_json_body(request):
    """Shared helper: safely parse JSON body, return (data, error_response)."""
    try:
        data = json.loads(request.body or "{}")
        return data, None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON body."}, status=400)


GMAIL_REGEX = re.compile(
    r"^[^\s@]+@gmail\.com$",
    re.IGNORECASE
)


def _validate_email_or_error(email):
    if not email:
        return JsonResponse(
            {"error": "Email is required."},
            status=400
        )

    email = email.strip().lower()

    # Only Gmail addresses are allowed.
    if not GMAIL_REGEX.fullmatch(email):
        return JsonResponse(
            {"error": "Please enter a valid Gmail address."},
            status=400
        )

    # Check whether the domain has MX records.
    if not _has_mx_record(email):
        return JsonResponse(
            {"error": "This email domain cannot receive email."},
            status=400
        )

    return None


# ------------------------------------------------------------------------
# Phase 3 — OTP send / verify / resend
# ------------------------------------------------------------------------

@csrf_exempt
@require_POST
def send_otp(request):
    """POST /api/otp/send/  { "email": "user@example.com" }"""
    data, error = _parse_json_body(request)
    if error:
        return error

    email = (data.get("email") or "").strip().lower()
    error = _validate_email_or_error(email)
    if error:
        return error

    # Cooldown check — applies to first send too, to stop rapid re-submits.
    existing = get_latest_otp(email)
    if existing and seconds_since_last_sent(existing) < settings.OTP_RESEND_COOLDOWN_SECONDS:
        remaining = int(settings.OTP_RESEND_COOLDOWN_SECONDS - seconds_since_last_sent(existing))
        return JsonResponse(
            {"error": f"Please wait {remaining} seconds before requesting another code."},
            status=429,
        )

    try:
        AuthUser.objects.get_or_create(email=email)
        issue_otp(email)
    except OTPDeliveryError:
        return JsonResponse(
            {"error": "We couldn't send the verification email. Please try again."},
            status=502,
        )
    except DatabaseError:
        return JsonResponse({"error": "Could not process request. Try again."}, status=503)

    return JsonResponse({"message": "Verification code generated successfully."})


@csrf_exempt
@require_POST
def verify_otp(request):
    """POST /api/otp/verify/  { "email": "user@example.com", "otp": "123456" }"""
    data, error = _parse_json_body(request)
    if error:
        return error

    email = (data.get("email") or "").strip().lower()
    otp_input = (data.get("otp") or "").strip()

    error = _validate_email_or_error(email)
    if error:
        return error
    if not otp_input:
        return JsonResponse({"error": "Please enter the complete 6-digit code."}, status=400)

    record = get_latest_otp(email)
    if not record or record.is_verified:
        return JsonResponse({"error": "No active verification code found. Request a new one."}, status=404)

    if record.is_expired():
        return JsonResponse(
            {"error": "Your verification code has expired. Please request a new code."},
            status=410,
        )

    if record.attempts >= settings.OTP_MAX_ATTEMPTS:
        return JsonResponse(
            {"error": "Too many incorrect attempts. Please request a new code."},
            status=429,
        )

    if not record.check_otp(otp_input):
        record.attempts += 1
        record.save(update_fields=["attempts"])
        return JsonResponse({"error": "Invalid verification code. Please try again."}, status=400)

    # Success.
    record.is_verified = True
    record.save(update_fields=["is_verified"])

    AuthUser.objects.filter(email=email).update(is_verified=True)

    return JsonResponse({"message": "Email verified successfully."})


@csrf_exempt
@require_POST
def resend_otp(request):
    """POST /api/otp/resend/  { "email": "user@example.com" }"""
    data, error = _parse_json_body(request)
    if error:
        return error

    email = (data.get("email") or "").strip().lower()
    error = _validate_email_or_error(email)
    if error:
        return error

    existing = get_latest_otp(email)
    if not existing:
        return JsonResponse({"error": "No verification session found for this email."}, status=404)

    elapsed = seconds_since_last_sent(existing)
    if elapsed < settings.OTP_RESEND_COOLDOWN_SECONDS:
        remaining = int(settings.OTP_RESEND_COOLDOWN_SECONDS - elapsed)
        return JsonResponse(
            {"error": f"Please wait {remaining} seconds before resending."},
            status=429,
        )

    try:
        issue_otp(email)
    except OTPDeliveryError:
        return JsonResponse(
            {"error": "We couldn't resend the verification email. Please try again."},
            status=502,
        )

    return JsonResponse({"message": "Verification code resent successfully."})