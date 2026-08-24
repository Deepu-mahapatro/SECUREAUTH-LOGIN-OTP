# SecureAuth — Testing Documentation

## 1. Testing Overview

SecureAuth was tested through the web interface and API requests using Postman.

The main goal was to verify email validation, OTP functionality, security controls, and database connectivity.

---

## 2. Email Validation Tests

| Test | Expected Result |
|---|---|
| Valid Gmail address | Accepted |
| Invalid email format | Rejected |
| Non-Gmail address | Rejected |
| Gmail domain typo | Rejected |
| Empty email | Rejected |

Example:

```text
user@gmail.com    → Accepted
user@yahoo.com    → Rejected
user@gamil.com    → Rejected

3. OTP Tests

Test	Expected Result
Correct OTP	Verification successful
Incorrect OTP	Error message displayed
Expired OTP	OTP rejected
Empty OTP	Request rejected
Too many attempts	Further attempts blocked

4. Resend OTP Tests

Test	Expected Result
Resend during cooldown	Request blocked
Resend after cooldown	New OTP sent
Resend without session	Request rejected

5. API Tests

The following endpoints were tested using Postman:

GET  /api/health/
GET  /api/auth/test/
POST /api/otp/send/
POST /api/otp/verify/
POST /api/otp/resend/
6. Database Test

The PostgreSQL connection was tested using the database test endpoint.

Expected result:

Database: connected

7. Security Tests

The following security features were tested:

✓ Gmail validation
✓ Backend email validation
✓ DNS MX checking
✓ OTP expiration
✓ OTP attempt limit
✓ OTP resend cooldown
✓ Secure OTP storage
✓ Environment variable protection

8. Final Testing Status

The main SecureAuth authentication workflow was tested successfully.

✓ Email validation
✓ OTP generation
✓ OTP delivery
✓ OTP verification
✓ OTP expiration
✓ OTP attempt limit
✓ OTP resend
✓ PostgreSQL connection
✓ API endpoints

9. Testing Tools

Web Browser
Postman
Django Development Server
PostgreSQL