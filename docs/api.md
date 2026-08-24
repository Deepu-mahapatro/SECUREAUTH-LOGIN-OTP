# SecureAuth — API Documentation

## Base URL

```text
http://127.0.0.1:8000
1. Health Check

Checks whether the Django backend is running.

Method: GET

Endpoint:

/api/health/

Response:

{
    "status": "ok",
    "message": "Backend is running"
}
2. Database Test

Checks whether Django is connected to PostgreSQL.

Method: GET

Endpoint:

/api/auth/test/

Response:

{
    "status": "ok",
    "database": "connected"
}
3. Send OTP

Generates and sends a 6-digit OTP to the user's Gmail address.

Method: POST

Endpoint:

/api/otp/send/

Request:

{
    "email": "user@gmail.com"
}

Success Response:

{
    "message": "Verification code generated successfully."
}
4. Verify OTP

Verifies the OTP entered by the user.

Method: POST

Endpoint:

/api/otp/verify/

Request:

{
    "email": "user@gmail.com",
    "otp": "123456"
}

Success Response:

{
    "message": "Email verified successfully."
}
5. Resend OTP

Sends a new OTP after the resend cooldown period.

Method: POST

Endpoint:

/api/otp/resend/

Request:

{
    "email": "user@gmail.com"
}

Success Response:

{
    "message": "Verification code resent successfully."
}
Common Error Codes
Code	Meaning
400	Invalid email, OTP, or request
404	Verification session not found
410	OTP expired
429	Too many attempts or resend too soon
502	Email delivery failed
503	Database/server problem
Authentication Flow
Send OTP
   ↓
User receives OTP
   ↓
Verify OTP
   ↓
Email Verified

The API handles the complete OTP verification process between the frontend, Django backend, email service, and database.
