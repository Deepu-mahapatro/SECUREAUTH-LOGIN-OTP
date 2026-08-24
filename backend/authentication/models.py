import hashlib

from django.db import models
from django.utils import timezone


class AuthUser(models.Model):
    """
    Minimal record of an email going through the verification flow.

    Fields:
    - email:       the address being verified. Unique so the same email
                    can't create duplicate rows — Django enforces this at
                    the database level with a UNIQUE constraint.
    - is_verified: False until the OTP step confirms the email. Kept
                    separate from OneTimePassword so we can query "who is
                    verified" cheaply without touching OTP records.
    - created_at:  when this email first entered the system. Set once,
                    never changes (auto_now_add).
    - updated_at:  last time this row changed (e.g. when is_verified
                    flips to True). Updates automatically on every save
                    (auto_now).
    """

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Normalize so "User@Example.com" and "user@example.com" are
        # always treated as the same record.
        self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({'verified' if self.is_verified else 'unverified'})"


class OneTimePassword(models.Model):
    """
    Fields:
    - email:        who the OTP was issued to. Not unique — a new row is
                     created every time an OTP is (re)sent.
    - otp_hash:      SHA-256 hash of the 6-digit code. We NEVER store the
                     plain code, the same way passwords are hashed — if the
                     database leaks, no valid codes are exposed.
    - created_at:    when this OTP was generated.
    - expires_at:    codes must not live forever; used to reject stale OTPs.
    - is_verified:   True once successfully used. A verified OTP can never
                     be verified again (blocks replay).
    - attempts:      failed verification attempts against this specific
                     OTP. Used to lock out brute-force guessing.
    - last_sent_at:  used to enforce the resend cooldown.
    """

    email = models.EmailField(db_index=True)
    otp_hash = models.CharField(max_length=64)  # SHA-256 hex digest = 64 chars

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_sent_at = models.DateTimeField(default=timezone.now)

    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "is_verified"]),
        ]

    def __str__(self):
        return f"OTP for {self.email} (verified={self.is_verified})"

    @staticmethod
    def hash_otp(raw_otp: str) -> str:
        return hashlib.sha256(raw_otp.encode("utf-8")).hexdigest()

    def check_otp(self, raw_otp: str) -> bool:
        return self.otp_hash == self.hash_otp(raw_otp)

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at