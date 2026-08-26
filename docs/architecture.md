SecureAuth — System Architecture
1. Overview

SecureAuth is a Django-based email OTP authentication system.

It connects the frontend, Django backend, PostgreSQL database, and Resend email API to provide a secure email verification workflow.

2. Architecture
User

  ↓

Frontend

HTML / CSS / JavaScript

  ↓

Django Backend

  ↓

Email Validation

  ↓

OTP Generation

  ↓

Resend Email API

  ↓

User Receives OTP

  ↓

OTP Verification

  ↓

PostgreSQL

  ↓

Email Verified
3. Main Components
Frontend

The frontend provides:

Email input
OTP input
Validation messages
Send verification code
Verify OTP
Resend OTP
Authentication success page

Technologies: HTML, CSS, JavaScript

Django Backend

The backend handles:

Email validation
OTP generation
OTP verification
OTP resend
OTP expiration
OTP attempt limitation
Authentication data
Session management
API request processing

Technology: Django

PostgreSQL

PostgreSQL stores:

User information
OTP records
Verification information
OTP-related data
Authentication-related records
Resend Email API

Resend is used to send the generated OTP to the user's email address.

The Django backend communicates with the Resend API using the configured API key and sender address.

Render

Render hosts the production Django application.

The production application connects to PostgreSQL and Resend using environment variables.

4. Authentication Process
1. User enters email address

             ↓

2. Frontend submits the email

             ↓

3. Django receives the request

             ↓

4. Django validates the email

             ↓

5. OTP is generated

             ↓

6. OTP is sent through Resend

             ↓

7. OTP information is stored in PostgreSQL

             ↓

8. User receives the OTP

             ↓

9. User enters the OTP

             ↓

10. Backend verifies the OTP

             ↓

11. OTP expiration and attempt limits are checked

             ↓

12. Email is marked as verified

             ↓

13. Success page is displayed
5. Security Flow
Email Validation

       ↓

OTP Generation

       ↓

OTP Storage

       ↓

OTP Expiration

       ↓

Attempt Limit

       ↓

Resend Cooldown

       ↓

OTP Verification

       ↓

Authentication Success

These layers help protect the authentication process from invalid email requests, expired verification codes, repeated OTP requests, and repeated OTP guessing attempts.

The OTP is only considered valid when it matches the expected verification information and satisfies the configured expiration and attempt restrictions.

6. Data Flow
User

  ↓

Frontend

  ↓

Django API

  ↓

Email Validation

  ↓

OTP Service

  ├──→ Resend API → User Email
  │
  └──→ PostgreSQL → OTP / User Data

The frontend communicates with the Django backend through API requests.

The Django backend validates the user's email and manages the OTP authentication process.

The backend communicates with the Resend API to deliver the OTP to the user's email.

At the same time, PostgreSQL stores the OTP-related information required for verification.

The OTP verification request is then sent from the frontend back to Django, where the stored OTP information is checked.

7. Result

After successful OTP verification:

OTP Verified

     ↓

User Email Verified

     ↓

Authentication Successful

     ↓

Success Page

This completes the SecureAuth email OTP authentication workflow.