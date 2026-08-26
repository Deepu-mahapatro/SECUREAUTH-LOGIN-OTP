SecureAuth — API Documentation
Base URL
http://127.0.0.1:8000

For production:

https://secureauth-login-otp.onrender.com
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

Generates and sends a 6-digit OTP to the user's email address through the Resend email service.

The OTP is also stored in the PostgreSQL database for verification.

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

The OTP is sent to the email address provided in the request.

The configured OTP expiration time, maximum attempts, and resend cooldown are applied during the OTP process.

4. Verify OTP

Verifies the OTP entered by the user.

The backend checks the submitted OTP against the OTP stored in PostgreSQL and validates its expiration and attempt restrictions.

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

If the OTP is incorrect, expired, or the maximum number of attempts has been reached, the API returns an appropriate error response.

5. Resend OTP

Sends a new OTP to the user's email address after the configured resend cooldown period.

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

The resend operation is controlled by the configured OTP resend cooldown to prevent repeated OTP requests.

Common Error Codes
Code	Meaning
400	Invalid email, OTP, or request
404	Verification session or OTP record not found
410	OTP expired
429	Too many attempts or OTP resend requested too soon
502	Email delivery failed
503	Database or server problem
Authentication Flow
Send OTP
    ↓
Django validates email
    ↓
Generate 6-digit OTP
    ↓
Store OTP in PostgreSQL
    ↓
Send OTP through Resend
    ↓
User receives OTP
    ↓
User enters OTP
    ↓
Verify OTP
    ↓
Email Verified
    ↓
Authentication Success

The API handles the complete OTP authentication process between the frontend, Django backend, PostgreSQL database, and Resend email service.