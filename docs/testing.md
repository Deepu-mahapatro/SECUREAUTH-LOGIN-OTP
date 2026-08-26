# SecureAuth — Testing Documentation

## 1. Testing Overview

SecureAuth was tested through the web interface, Django API endpoints, PostgreSQL database connection, Resend email delivery service, and after production deployment.

The main goal was to verify the complete email OTP authentication workflow, including email validation, DNS/MX validation, OTP generation and delivery, OTP verification, OTP expiration, resend functionality, attempt limitation, PostgreSQL connectivity, static file handling, production deployment, and environment configuration.

---

## 2. Email Validation Tests

| Test                          | Expected Result                  |
| ----------------------------- | -------------------------------- |
| Open authentication page      | Page loads successfully          |
| Valid email address            | Email accepted                   |
| Invalid email format           | Email rejected                   |
| Invalid Gmail address          | Email rejected                   |
| Email domain typo              | Email rejected                   |
| Empty email                    | Request rejected                 |
| DNS/MX validation              | Domain validation completed      |

Example:

```text
Open Authentication Page    → Page Loaded

Enter Valid Gmail           → Email Accepted

Invalid Email Format        → Request Rejected

Invalid Domain              → Request Rejected

DNS / MX Check              → Domain Validated
3. OTP Tests
Test	Expected Result
OTP generation	Six-digit OTP generated
Correct OTP	Verification successful
Incorrect OTP	Error message displayed
Expired OTP	OTP rejected
Empty OTP	Request rejected
Invalid OTP format	Request rejected
Too many attempts	Further attempts blocked
OTP delivery	OTP received by user

The OTP verification process checks the submitted code against the OTP information stored by the backend.

The configured OTP expiration time and maximum attempt limit are also applied during verification.

4. Resend OTP Tests
Test	Expected Result
Resend during cooldown	Request blocked
Resend after cooldown	New OTP sent
Invalid email	Request rejected
Verification session missing	Request rejected
Valid resend request	New verification code generated

The resend functionality uses the configured OTP resend cooldown to prevent users from repeatedly requesting verification codes within a short period.

5. API Tests

The following SecureAuth API endpoints were tested during development:

GET  /api/health/

GET  /api/auth/test/

POST /api/otp/send/

POST /api/otp/verify/

POST /api/otp/resend/

The health check endpoint was tested to verify that the Django backend was running.

The database test endpoint was tested to verify PostgreSQL connectivity.

The send OTP endpoint was tested to verify email validation, OTP generation, and email delivery.

The verify OTP endpoint was tested to verify OTP validation, expiration handling, and attempt limitation.

The resend OTP endpoint was tested to verify resend cooldown and new OTP generation.

6. OTP Authentication Success Test

The successful email OTP authentication flow was tested from the initial email submission through OTP delivery and verification.

Expected result:

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

User Enters OTP

        ↓

Django OTP Verification

        ↓

Email Verified

        ↓

Authentication Success

The user was successfully redirected to the authentication success page after entering a valid OTP.

7. Security Tests

The following security features were tested:

✓ Email format validation

✓ Backend email validation

✓ Gmail domain validation

✓ DNS / MX record validation

✓ Six-digit OTP generation

✓ OTP expiration

✓ OTP attempt limitation

✓ OTP resend cooldown

✓ Secure OTP processing

✓ PostgreSQL OTP storage

✓ Backend request validation

✓ Authentication error handling

✓ Environment variable protection

✓ .env exclusion from Git

✓ Resend API key protection

✓ Django secret key protection

✓ Database credential protection

Sensitive Resend API credentials, database credentials, and Django configuration values were kept outside the source code using environment variables.

The .env file is excluded from Git to prevent sensitive configuration from being exposed.

8. Database Tests

The production application uses PostgreSQL.

The following database functionality was verified:

✓ PostgreSQL database connection

✓ Django database configuration

✓ Database migrations

✓ User data storage

✓ OTP data storage

✓ Verification status storage

✓ Authentication-related database operations

The production PostgreSQL database is configured through the Render production environment.

The database connection was also verified through:

GET /api/auth/test/

Expected result:

Database: connected
9. Email Delivery Tests

The Resend email integration was tested to verify that generated OTPs could be delivered to the user's email address.

The following functionality was verified:

✓ Resend API key configuration

✓ Sender email configuration

✓ OTP generation

✓ OTP email delivery

✓ Email received by the user

✓ OTP verification after email delivery

✓ OTP resend

The production application was also tested with the Resend email service after deployment on Render.

10. Static File Tests

Static files were tested after production deployment.

The following functionality was verified:

✓ CSS files load correctly

✓ JavaScript files load correctly

✓ Static files collected successfully

✓ WhiteNoise static file serving

✓ Static files accessible from production

Static files are collected during deployment using Django's collectstatic command and served through WhiteNoise.

11. Production Deployment Tests

The deployed application was tested on the Render production environment.

Production URL:

https://secureauth-login-otp.onrender.com/

The following production functionality was verified:

✓ Application loads successfully

✓ Production HTTPS connection

✓ Authentication page loads

✓ Static files load correctly

✓ Email validation works

✓ DNS / MX validation works

✓ OTP generation works

✓ OTP email delivery works

✓ OTP verification works

✓ OTP expiration works

✓ OTP attempt limitation works

✓ OTP resend works

✓ Resend cooldown works

✓ PostgreSQL connection works

✓ Authentication success page loads

✓ API endpoints respond correctly

✓ Authentication error handling works

Production API Base URL:

https://secureauth-login-otp.onrender.com
12. Final Testing Status

The main SecureAuth authentication workflow was tested successfully.

✓ Authentication page

✓ Email validation

✓ Gmail validation

✓ DNS / MX validation

✓ OTP generation

✓ OTP email delivery

✓ OTP verification

✓ OTP expiration

✓ OTP attempt limitation

✓ OTP resend

✓ Resend cooldown

✓ PostgreSQL database connection

✓ API endpoints

✓ Authentication success

✓ Static file loading

✓ Production deployment

✓ Render production environment

✓ Resend email integration

✓ Authentication error handling

✓ Environment variable configuration

The complete authentication flow was successfully tested from email submission through validation, OTP generation, email delivery, OTP verification, email verification, authentication success, and production deployment.

13. Testing Tools
Web Browser

Used to test the complete SecureAuth user interface and authentication workflow.

Postman

Used to test the Django API endpoints independently from the frontend.

Django Development Server

Used to test the application locally during development.

http://127.0.0.1:8000/
PostgreSQL

Used to verify database connectivity and OTP-related database operations.

Resend

Used to test OTP email delivery during local development and production.

DNS / MX Resolver

Used to validate whether the email domain is configured to receive email.

Render

Used to test the deployed production application and its connection with PostgreSQL and Resend.

Gunicorn

Used as the production WSGI server for the Django application.

WhiteNoise

Used to serve Django static files in the production environment.