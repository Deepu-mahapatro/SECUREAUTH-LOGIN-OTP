# SecureAuth — API Documentation

## Base URLs

### Local Development

```text
http://127.0.0.1:8000
Production
https://secureauth-login-otp.onrender.com
Live Application
https://secureauth-login-otp.onrender.com/
1. Health Check

Checks whether the SecureAuth Django backend is running.

Method: GET

Endpoint:

/api/health/

Production Endpoint:

https://secureauth-login-otp.onrender.com/api/health/

Response:

{
    "status": "ok",
    "message": "Backend is running"
}

The endpoint is used to confirm that the production Django application is running correctly.

Django Application

   ↓

Health Check Endpoint

   ↓

Backend Running

The endpoint does not require authentication and is intended for application health verification.

2. Database Test

Checks whether Django can successfully communicate with the configured PostgreSQL database.

Method: GET

Endpoint:

/api/auth/test/

Production Endpoint:

https://secureauth-login-otp.onrender.com/api/auth/test/

Response:

{
    "status": "ok",
    "database": "connected"
}

The endpoint performs a real database query to verify PostgreSQL connectivity.

Django Application

   ↓

PostgreSQL Connection

   ↓

Database Query

   ↓

Database Connected

The endpoint is useful for verifying that the production application can communicate with its PostgreSQL database.

3. Send OTP

Generates and sends a six-digit verification code to the user's email address.

Method: POST

Endpoint:

/api/otp/send/

Production Endpoint:

https://secureauth-login-otp.onrender.com/api/otp/send/

Request:

{
    "email": "user@gmail.com"
}

Processing Flow:

User Email

       ↓

Django Backend

       ↓

Email Format Validation

       ↓

Gmail Validation

       ↓

DNS / MX Record Check

       ↓

OTP Generation

       ↓

PostgreSQL

       ↓

Resend Email API

       ↓

User Receives OTP

Response:

{
    "message": "Verification code generated successfully."
}

The endpoint validates the submitted email address before generating the OTP.

The backend performs email validation and DNS/MX domain verification before the OTP delivery process.

After successful validation, Django generates the six-digit OTP and sends it through the configured Resend email service.

OTP-related information is stored in PostgreSQL for later verification.

The configured OTP expiration, maximum attempt limit, and resend cooldown are applied during the authentication process.

4. Verify OTP

Verifies the OTP entered by the user.

Method: POST

Endpoint:

/api/otp/verify/

Production Endpoint:

https://secureauth-login-otp.onrender.com/api/otp/verify/

Request:

{
    "email": "user@gmail.com",
    "otp": "123456"
}

Response:

{
    "message": "Email verified successfully."
}

The backend checks the submitted OTP against the OTP information stored in PostgreSQL.

During verification, Django checks:

OTP validity
OTP expiration
OTP attempt limit
Verification status

Verification Flow:

User Enters OTP

       ↓

Django Verification Endpoint

       ↓

Find Latest OTP

       ↓

Check OTP Expiration

       ↓

Check Attempt Limit

       ↓

Verify OTP

       ↓

Email Marked as Verified

       ↓

Authentication Success

If the OTP is incorrect, expired, or the maximum number of attempts has been reached, the backend returns an appropriate error response.

5. Resend OTP

Generates and sends a new verification code to the user's email address.

Method: POST

Endpoint:

/api/otp/resend/

Production Endpoint:

https://secureauth-login-otp.onrender.com/api/otp/resend/

Request:

{
    "email": "user@gmail.com"
}

Response:

{
    "message": "Verification code resent successfully."
}

The resend operation is controlled by the configured OTP resend cooldown.

The backend checks whether a verification session exists and whether the required cooldown period has passed before generating another OTP.

Resend Flow:

User Requests Resend

       ↓

Django Backend

       ↓

Verification Session Check

       ↓

Resend Cooldown Check

       ↓

Generate New OTP

       ↓

Resend Email API

       ↓

User Receives New OTP

If the user requests another OTP before the cooldown period has completed, the request is rejected.

Common Error Responses
Code	Meaning
400	Invalid email, OTP, or request
404	Verification session or OTP record not found
410	OTP expired
429	Too many attempts or OTP resend requested too soon
502	Email delivery failed
503	Database or server problem
Authentication Flow

Email Authentication

↓

Email Submission

↓

Django Backend

↓

Email Validation

↓

DNS / MX Record Verification

↓

OTP Generation

↓

PostgreSQL Database

↓

Resend Email API

↓

User Receives OTP

↓

OTP Submission

↓

OTP Verification

↓

OTP Expiration Check

↓

OTP Attempt Limit Check

↓

Email Verified

↓

Authentication Success

The API handles the complete email OTP authentication process between the frontend, Django backend, PostgreSQL database, DNS validation service, Resend email service, and authentication workflow.

Production Deployment

The application is deployed using Render.

Production Application:

https://secureauth-login-otp.onrender.com/

Production API Base URL:

https://secureauth-login-otp.onrender.com

Production Architecture:

User

   ↓

SecureAuth Frontend

   ↓

Django Backend

   ↓

Email Validation

   ↓

OTP Service

   ├──→ Resend API → User Email
   │
   └──→ PostgreSQL → OTP / User Data

   ↓

OTP Verification

   ↓

Email Verified

   ↓

Authentication Success

The production application uses environment variables for sensitive configuration such as the Django secret key, PostgreSQL connection details, and Resend API credentials.

The production environment is hosted on Render with PostgreSQL configured for persistent authentication and OTP-related data.