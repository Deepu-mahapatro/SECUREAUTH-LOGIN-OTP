SecureAuth — Testing Documentation
1. Testing Overview

SecureAuth was tested through the web interface, Django API requests, PostgreSQL database connection, and the Resend email service.

The main goal was to verify email validation, OTP generation and delivery, OTP verification, security controls, resend functionality, API endpoints, and database connectivity.

2. Email Validation Tests
Test	Expected Result
Valid email address	Accepted
Invalid email format	Rejected
Unsupported/invalid email address	Rejected
Email domain typo	Rejected
Empty email	Rejected

Example:

user@gmail.com       → Accepted

user@               → Rejected

usergmail.com       → Rejected

user@gamil.com      → Rejected

(empty email)       → Rejected

The email validation is performed before the OTP generation process begins.

3. OTP Tests
Test	Expected Result
Correct OTP	Verification successful
Incorrect OTP	Error message displayed
Expired OTP	OTP rejected
Empty OTP	Request rejected
Invalid OTP format	Request rejected
Too many attempts	Further attempts blocked

The OTP verification process checks the submitted code against the OTP information stored by the backend.

The configured OTP expiration time and maximum attempt limit are also applied during verification.

4. Resend OTP Tests
Test	Expected Result
Resend during cooldown	Request blocked
Resend after cooldown	New OTP sent
Invalid email	Request rejected
Resend request processed successfully	New verification code generated

The resend functionality uses the configured OTP resend cooldown to prevent users from repeatedly requesting verification codes within a short period.

5. API Tests

The following endpoints were tested through the Django application and browser/API requests:

GET  /api/health/

GET  /api/auth/test/

POST /api/otp/send/

POST /api/otp/verify/

POST /api/otp/resend/
Health Check
GET /api/health/

Expected result:

{
    "status": "ok",
    "message": "Backend is running"
}
Database Test
GET /api/auth/test/

Expected result:

{
    "status": "ok",
    "database": "connected"
}
Send OTP
POST /api/otp/send/

Expected result:

{
    "message": "Verification code generated successfully."
}
Verify OTP
POST /api/otp/verify/

Expected result:

{
    "message": "Email verified successfully."
}
Resend OTP
POST /api/otp/resend/

Expected result:

{
    "message": "Verification code resent successfully."
}
6. Database Test

The PostgreSQL connection was tested using the database test endpoint.

Expected result:

Database: connected

The database testing confirms that Django can communicate with the configured PostgreSQL database.

The project was tested with PostgreSQL during local development and with the production PostgreSQL database configured through Render.

7. Email Delivery Tests

The Resend email integration was tested to verify that generated OTPs could be delivered to the user's email address.

The following operations were tested:

✓ Resend API key configuration

✓ Sender email configuration

✓ OTP generation

✓ OTP email delivery

✓ Email received by the user

✓ OTP verification after email delivery

The production application was also tested with the Resend API after deployment on Render.

8. Security Tests

The following security features were tested:

✓ Email validation

✓ Backend email validation

✓ Six-digit OTP generation

✓ OTP expiration

✓ OTP attempt limit

✓ OTP resend cooldown

✓ OTP verification

✓ Secure OTP processing

✓ PostgreSQL OTP storage

✓ Environment variable protection

✓ Resend API key protection

✓ Django secret key protection

✓ Database credential protection

The security controls help prevent invalid requests, expired OTP usage, repeated OTP guessing, and excessive OTP resend requests.

9. Final Testing Status

The main SecureAuth authentication workflow was tested successfully.

✓ Email validation

✓ OTP generation

✓ OTP delivery

✓ OTP verification

✓ OTP expiration

✓ OTP attempt limit

✓ OTP resend

✓ Resend email API

✓ PostgreSQL connection

✓ API endpoints

✓ Authentication success

✓ Authentication error handling

✓ Local development environment

✓ Production deployment

✓ Render production environment

✓ Static file serving

10. Testing Tools
Web Browser

Used to test the complete SecureAuth user interface and authentication workflow.

Postman / API Requests

Used to test the Django API endpoints independently from the frontend.

Django Development Server

Used to test the application locally during development.

http://127.0.0.1:8000/
PostgreSQL

Used to verify database connectivity and OTP-related database operations.

Resend

Used to test OTP email delivery during local development and production.

Render

Used to test the deployed production application and its connection with PostgreSQL and Resend.

The production application was tested at:

https://secureauth-login-otp.onrender.com