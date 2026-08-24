# SecureAuth — System Architecture

## 1. Overview

SecureAuth is a Django-based email OTP authentication system.

It connects the frontend, Django backend, PostgreSQL database, Gmail SMTP, and DNS MX validation to provide a secure email verification workflow.

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
Gmail + MX Check
  ↓
OTP Generation
  ↓
Gmail SMTP
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
Verify OTP
Resend OTP
Success page

Technologies: HTML, CSS, JavaScript

Django Backend

The backend handles:

Email validation
Gmail validation
DNS MX checking
OTP generation
OTP verification
OTP resend
Authentication data

Technology: Django

PostgreSQL

PostgreSQL stores:

User information
OTP records
Verification status
OTP-related data
Gmail SMTP

Gmail SMTP is used to send the generated OTP to the user's email address.

DNS MX Check

DNS MX records are checked to determine whether the email domain is configured to receive emails.

4. Authentication Process
1. User enters Gmail address
             ↓
2. Frontend validates the email
             ↓
3. Django validates the email
             ↓
4. Gmail and MX validation
             ↓
5. OTP is generated
             ↓
6. OTP is sent through Gmail SMTP
             ↓
7. User enters the OTP
             ↓
8. Backend verifies the OTP
             ↓
9. Email is marked as verified
             ↓
10. Success page is displayed
5. Security Flow
Email Validation
       ↓
Gmail Validation
       ↓
DNS MX Check
       ↓
OTP Generation
       ↓
OTP Hashing
       ↓
OTP Expiration
       ↓
Attempt Limit
       ↓
OTP Verification

These layers help protect the authentication process from invalid requests and repeated OTP guessing.

6. Data Flow
User
 ↓
Django API
 ↓
Validation
 ↓
OTP Service
 ├──→ Gmail SMTP → User Email
 │
 └──→ PostgreSQL → OTP/User Data

The frontend communicates with the Django backend, while the backend manages OTP delivery and database operations.

7. Result

After successful OTP verification:

OTP Verified
     ↓
User Email Verified
     ↓
Success Page

This completes the SecureAuth email verification workflow.
