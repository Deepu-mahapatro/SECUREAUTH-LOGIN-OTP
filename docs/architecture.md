# SecureAuth — System Architecture

## 1. Overview

SecureAuth is a Django-based email OTP authentication system.

It connects the frontend, Django backend, email validation, OTP service, Resend email API, PostgreSQL database, and authentication workflow to provide a secure email-based verification system.

The system allows users to verify their email address using a time-limited One-Time Password (OTP) instead of relying on a traditional password-based authentication flow.

The application is deployed in a production environment using Render, Gunicorn, PostgreSQL, and WhiteNoise.

---

## 2. Architecture

```text
User

  ↓

Frontend

HTML / CSS / JavaScript

  ↓

Django Backend

  ↓

Email Validation

  ↓

DNS / MX Record Verification

  ↓

OTP Generation

  ↓

Resend Email API

  ↓

User Receives OTP

  ↓

OTP Verification

  ↓

PostgreSQL Database

  ↓

Email Verified

  ↓

Authentication Success
3. Main Components
Frontend

The frontend provides:

Email input
Email validation messages
Send verification code
OTP input
OTP verification
Resend OTP
Verification status
Authentication success page
User interaction and navigation

Technologies: HTML, CSS, JavaScript

Django Backend

The backend handles:

URL routing
Email validation
Gmail validation
DNS / MX record validation
OTP generation
OTP delivery
OTP verification
OTP expiration
OTP attempt limitation
OTP resend cooldown
Authentication data
User verification status
API request processing
Database operations
Authentication success handling
Error handling

Technology: Django

Email Validation

The email validation layer checks whether the submitted email address is valid before the OTP process begins.

It handles:

Email syntax validation
Gmail address validation
Email domain validation
DNS resolution
MX record verification

The validation process helps prevent malformed or unsupported email addresses from entering the OTP authentication workflow.

OTP Service

The OTP service is responsible for generating and managing verification codes.

It handles:

Six-digit OTP generation
OTP storage
OTP expiration
OTP verification
OTP attempt limitation
OTP resend
Resend cooldown

The OTP information required for verification is stored in PostgreSQL.

Resend Email API

Resend is used to deliver generated OTP codes to the user's email address.

The Django backend communicates with the Resend API using the configured API key and sender configuration.

The Resend service handles:

OTP email delivery
Email transmission
Verification code delivery

PostgreSQL

PostgreSQL is used as the production database for SecureAuth.

The database stores:

User information
OTP records
Verification information
OTP-related data
Authentication-related records

Django manages communication with PostgreSQL through its database layer.

The production PostgreSQL database is configured through the Render production environment.

Gunicorn

Gunicorn is used as the production WSGI server.

It runs the Django application in the Render production environment.

Render Web Service

       ↓

Gunicorn

       ↓

Django Application
WhiteNoise

WhiteNoise is used to serve Django static files in the production environment.

Static files are collected during deployment and served through WhiteNoise.

Django Static Files

       ↓

collectstatic

       ↓

WhiteNoise

       ↓

Production Browser
Render

Render provides the production hosting environment for SecureAuth.

The deployment uses:

Render Web Service for Django
Render PostgreSQL for the database
Gunicorn for the production WSGI server
WhiteNoise for static files
Environment variables for sensitive configuration

4. Authentication Process

User opens the authentication page

      ↓

User enters an email address

      ↓

Frontend submits the email

      ↓

Django receives the request

      ↓

Django validates the email format

      ↓

Django validates the Gmail address

      ↓

Django checks DNS / MX records

      ↓

Django generates a six-digit OTP

      ↓

OTP information is stored in PostgreSQL

      ↓

Django sends the OTP through Resend

     ↓

User receives the verification code

     ↓

User enters the OTP

     ↓

Django receives the OTP verification request

     ↓

Django checks the OTP

     ↓

Django checks OTP expiration

     ↓

Django checks the maximum attempt limit

     ↓

OTP is verified

     ↓

User email is marked as verified

     ↓
User is redirected to the success page
5. Security Flow

Email Validation

   ↓

DNS / MX Record Validation

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

OTP Delivery

   ↓

OTP Verification

   ↓

Email Verification

   ↓

Authentication Success

These layers help protect the authentication process from invalid email requests, unsupported domains, expired verification codes, repeated OTP requests, and repeated OTP guessing attempts.

The backend performs email validation before the OTP generation process begins.

DNS/MX validation is used to determine whether the email domain is configured to receive email.

OTP expiration prevents an old verification code from being used after its configured validity period.

The maximum attempt limit helps prevent repeated OTP guessing.

The resend cooldown prevents users from repeatedly requesting new verification codes within a short period.

Sensitive configuration values such as the Django secret key, database credentials, and Resend API credentials are stored using environment variables instead of being hardcoded into the application.

The .env file is excluded from Git to prevent sensitive credentials from being exposed.

Production environment variables are configured securely through Render.

6. Data Flow

User

↓

SecureAuth Frontend

↓

Django Backend

↓

Email Validation

↓

DNS / MX Record Verification

↓

OTP Generation

├──→ Resend API → User Email
│
└──→ PostgreSQL → OTP / User Data

↓

User Receives OTP

↓

OTP Verification Request

↓

Django Backend

↓

OTP Validation

↓

Expiration Check

↓

Attempt Limit Check

↓

Email Verified

↓

Authentication Success

↓

Success Page

The frontend communicates with the Django backend through API requests.

The Django backend receives the submitted email address and performs server-side validation.

The email domain is checked through DNS/MX validation before the OTP is generated.

After successful validation, Django generates a six-digit OTP.

The OTP information is stored in PostgreSQL while the verification code is delivered to the user through the Resend email service.

The user enters the received OTP and sends the verification request back to Django.

Django retrieves the latest OTP information and checks the submitted code, expiration status, and attempt restrictions.

After successful verification, the user's email is marked as verified and the user is redirected to the authentication success page.

PostgreSQL stores the required user, OTP, and verification-related data.

7. Production Architecture

The application is deployed using Render.

User Browser

      ↓

Render Web Service

      ↓

Gunicorn

      ↓

Django Application

      ├──────────────→ DNS / MX Validation
      │
      ├──────────────→ Resend Email API
      │
      ↓
PostgreSQL Database

      ↓

OTP Verification

      ↓

Email Verified

      ↓

Authentication Success
Production URL
https://secureauth-login-otp.onrender.com/
Production API Base URL
https://secureauth-login-otp.onrender.com
Production Email Flow
Django Application

       ↓

Generate OTP

       ↓

Resend API

       ↓

User Email

       ↓

OTP Received

       ↓

OTP Submitted

       ↓

Django Verification

       ↓

Email Verified
Production Database
Django Application

       ↓

PostgreSQL

       ↓

User Data

OTP Data

Verification Data
Production Static Files
Django Static Files

       ↓

collectstatic

       ↓

WhiteNoise

       ↓

Render

       ↓

Production Browser
8. Deployment Flow

Developer

↓

VS Code

↓

Git

↓

GitHub

↓

Render

↓

Install Dependencies

↓

Configure Environment Variables

↓

Run Database Migrations

↓

Collect Static Files

↓

Gunicorn

↓

Django Application

↓

Render PostgreSQL

↓

Resend Email API

↓

Live Application

The application source code is maintained in GitHub.

Render deploys the application from the GitHub repository.

During deployment, Django dependencies are installed, production environment variables are configured, database migrations are applied, and static files are collected.

WhiteNoise serves the collected static files in the production environment.

Gunicorn then starts the Django production application.

The running Django application communicates with PostgreSQL for persistent data and with the Resend API for OTP email delivery.

The production application is available through the Render deployment URL.

9. Result

After successful OTP verification:

Email Submission

   ↓

Email Validation

   ↓

DNS / MX Validation

   ↓

OTP Generation

   ↓

OTP Delivery

   ↓

OTP Verification

   ↓

OTP Expiration Check

   ↓

Attempt Limit Check

   ↓

Email Verified

   ↓

Authentication Success

   ↓

Success Page

After requesting a new OTP:

User

       ↓

Resend OTP Request

       ↓

Cooldown Check

       ↓

New OTP Generated

       ↓

Resend Email API

       ↓

New OTP Delivered

       ↓

OTP Verification

This completes the SecureAuth email OTP authentication workflow