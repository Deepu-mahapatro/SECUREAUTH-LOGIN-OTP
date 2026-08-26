# SecureAuth — Email OTP Authentication System

SecureAuth is a Django-based authentication system designed to provide secure email-based user verification using **One-Time Passwords (OTP)**.

The project implements a complete email verification workflow, including email validation, DNS/MX domain verification, OTP generation, OTP delivery through the Resend email service, OTP verification, expiration handling, resend protection, attempt limitation, PostgreSQL database integration, and authentication success handling.

Built with a production-oriented architecture for **educational, portfolio, and real-world authentication workflow demonstration purposes**.

## 🌐 Live Demo

**Live Application:**

https://secureauth-login-otp.onrender.com/

**Source Code:**

https://github.com/Deepu-mahapatro/SECUREAUTH-LOGIN-OTP.git

## 📌 Overview

SecureAuth provides a complete email OTP authentication workflow instead of relying only on basic email format validation.

Users enter their email address through the authentication interface. The Django backend validates the email, checks the domain's DNS/MX configuration, generates a secure one-time verification code, and sends the OTP through the configured Resend email service.

The OTP information is stored in PostgreSQL and is later used to verify the code submitted by the user.

The system also applies OTP expiration, maximum verification attempts, resend cooldown protection, backend validation, and environment-based credential management.

After successful verification, the user's email is marked as verified and the authentication workflow proceeds to the success page.

## ✨ Features

- Email-based authentication
- Email address validation
- Gmail email validation
- Backend email validation
- DNS domain verification
- MX record validation
- One-Time Password (OTP) generation
- Six-digit OTP authentication
- OTP email delivery
- Resend email service integration
- OTP expiration handling
- OTP verification
- OTP attempt limitation
- OTP resend cooldown
- Secure OTP processing
- PostgreSQL database integration
- User verification status management
- Authentication success page
- Authentication error handling
- API-based backend communication
- Environment variable configuration
- `.env` credential protection
- Server-side validation
- Production deployment with Render
- PostgreSQL production database
- Static file serving
- Browser-based authentication testing

## 🔐 Authentication Flow

```text
User
     ↓
Open Authentication Page
     ↓
Enter Email Address
     ↓
Frontend Validation
     ↓
Django Backend
     ↓
Email Validation
     ↓
DNS / MX Domain Validation
     ↓
Generate 6-Digit OTP
     ↓
Store OTP Information
     ↓
Send OTP through Resend
     ↓
User Receives OTP
     ↓
Enter OTP
     ↓
Backend OTP Verification
     ↓
Check Expiration
     ↓
Check Attempt Limit
     ↓
OTP Valid
     ↓
Email Marked as Verified
     ↓
Authentication Success
Email OTP Flow
Browser
    │
    ▼
Django Application
    │
    ▼
POST /api/otp/send/
    │
    ▼
Email Validation
    │
    ▼
DNS Resolver
    │
    ▼
MX Record Verification
    │
    ▼
OTP Generation
    │
    ├──────────────→ Resend Email API
    │                         │
    │                         ▼
    │                    User Email
    │
    ▼
PostgreSQL
    │
    ▼
OTP Information Stored
    │
    ▼
User Enters OTP
    │
    ▼
POST /api/otp/verify/
    │
    ▼
OTP Validation
    │
    ▼
Email Verified
    │
    ▼
Authentication Success

The authentication process starts when the user enters an email address.

The frontend sends the email to the Django backend.

Django performs server-side email validation and verifies the email domain using DNS/MX record validation.

After successful validation, a six-digit OTP is generated and delivered through the configured Resend email service.

The OTP information is stored in PostgreSQL for verification.

The user enters the received OTP and submits it to the backend.

Django checks the OTP, expiration status, and maximum attempt limit.

After successful verification, the user's email is marked as verified and the authentication process is completed.

🛠️ Technology Stack
Technology	Purpose
Python	Programming Language
Django	Backend Web Framework
HTML5	Frontend
CSS3	Styling
JavaScript	Frontend Logic
PostgreSQL	Production Database
Resend	OTP Email Delivery
dnspython	DNS / MX Record Validation
Django Sessions	Session Management
python-dotenv	Environment Configuration
Postman	API Testing
Git & GitHub	Version Control
Render	Production Deployment
📂 Project Structure
SECUREAUTH-LOGIN-OTP/
│
├── README.md
├── .gitignore
│
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    │
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── authentication/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── utils.py
    │   └── ...
    │
    ├── templates/
    │   ├── index.html
    │   ├── verify.html
    │   └── success.html
    │
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            └── script.js

The project is organized into a Django backend, authentication application, templates, static frontend assets, configuration files, and environment-based settings.

The authentication application contains the core email validation, OTP generation, OTP verification, resend, and database logic.

The .env file is used for sensitive local and production configuration and is excluded from Git.

🔗 API Endpoints

Health Check
GET /api/health/

Checks whether the Django backend is running.

Expected response:

{
    "status": "ok",
    "message": "Backend is running"
}
Database Test
GET /api/auth/test/

Checks whether Django can successfully communicate with PostgreSQL.

Expected response:

{
    "status": "ok",
    "database": "connected"
}
Send OTP
POST /api/otp/send/

Generates and sends a six-digit OTP to the user's email address.

Request:

{
    "email": "user@gmail.com"
}

Success response:

{
    "message": "Verification code sent successfully."
}

The endpoint validates the email address before generating and delivering the OTP.

The configured OTP expiration, maximum attempt limit, and resend cooldown are applied during the authentication process.

Verify OTP
POST /api/otp/verify/

Verifies the OTP submitted by the user.

Request:

{
    "email": "user@gmail.com",
    "otp": "123456"
}

Success response:

{
    "message": "Email verified successfully."
}

The backend checks the submitted OTP against the stored OTP information and validates expiration and attempt restrictions.

Resend OTP
POST /api/otp/resend/

Generates and sends a new verification code after the configured resend cooldown period.

Request:

{
    "email": "user@gmail.com"
}

Success response:

{
    "message": "Verification code resent successfully."
}

The resend operation is protected by the configured cooldown period to prevent repeated OTP requests.

Common Error Codes
Code	Meaning
400	Invalid email, OTP, or request
404	Verification session or OTP record not found
410	OTP expired
429	Too many attempts or OTP resend requested too soon
502	Email delivery failed
503	Database or server problem
🛡️ Security Features
Server-side email validation
Email format validation
Gmail domain validation
DNS-based domain verification
MX record verification
Six-digit OTP authentication
OTP expiration
OTP attempt limitation
OTP resend cooldown
Secure OTP processing
PostgreSQL-backed OTP storage
Environment-based secret management
.env excluded from Git
No sensitive credentials hardcoded in source code
Resend API key protection
Django secret key protection
Database credential protection
Backend request validation
Authentication error handling
Production HTTPS deployment

The application performs validation on the backend rather than relying only on frontend validation.

The email domain is checked through DNS/MX validation before the OTP delivery process begins.

OTP verification is additionally protected by expiration and maximum attempt restrictions.

Repeated OTP requests are controlled through the configured resend cooldown.

Sensitive configuration values are stored through environment variables.

Example:

SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-production-database-url
RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=your-verified-sender

The actual .env file must never be uploaded to GitHub.

⚙️ Installation

1. Clone the Repository
git clone https://github.com/Deepu-mahapatro/SECUREAUTH-LOGIN-OTP.git
2. Open the Backend
cd SECUREAUTH-LOGIN-OTP/backend
3. Create Virtual Environment
python -m venv venv
4. Activate Virtual Environment

Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file inside the backend directory.

Example:

SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_URL=your-database-url

RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=your-verified-sender-email

For production, configure the corresponding environment variables through the Render service configuration.

Never upload your actual .env file or API credentials to GitHub.

🗄️ Database Setup

The project uses PostgreSQL for persistent authentication and OTP-related data.

After configuring the database environment variables, run:

python manage.py makemigrations

Then apply the migrations:

python manage.py migrate

Django creates the required database tables used by the authentication system, including user and OTP-related records.

The database connection can be verified using:

GET /api/auth/test/

Expected result:

{
    "status": "ok",
    "database": "connected"
}
▶️ Run the Project

Start the Django development server:

python manage.py runserver

Open:

http://127.0.0.1:8000/

The SecureAuth email authentication page will be displayed.

Enter a valid Gmail address and start the verification process.

The application will validate the email, generate an OTP, deliver the code through the configured email service, and redirect the user to the OTP verification page.

After successful OTP verification, the user is redirected to the authentication success page.

🚀 Production Deployment

SecureAuth is deployed as a production application using Render.

Production application:

https://secureauth-login-otp.onrender.com/

The production environment uses:

User
    ↓
SecureAuth Frontend
    ↓
Django Application
    ↓
Email Validation
    ↓
OTP Generation
    ↓
Resend Email Service
    ↓
PostgreSQL
    ↓
OTP Verification
    ↓
Authentication Success

Before production deployment, configure:

DEBUG=False
Production SECRET_KEY
Production DATABASE_URL
Resend API credentials
Verified sender email
Allowed hosts
HTTPS configuration
Secure session configuration
CSRF configuration

Production secrets should be configured through Render environment variables rather than stored in the source code.

🧪 Testing

The SecureAuth authentication workflow was tested through the web interface, Django API endpoints, PostgreSQL database connection, and Resend email delivery service.

Tested cases include:

Application startup
Authentication page
Valid email address
Invalid email format
Unsupported email address
Email domain typo
Empty email
DNS resolution
MX record validation
OTP generation
OTP email delivery
Correct OTP verification
Incorrect OTP handling
Expired OTP handling
Empty OTP handling
Invalid OTP format
Maximum OTP attempts
OTP resend
Resend cooldown
PostgreSQL connection
API endpoint responses
Authentication success
Authentication error handling
Environment variable configuration
Resend API configuration
Production deployment
Render production environment
Static file serving
Email Validation Test
user@gmail.com
        ↓
Accepted

user@
        ↓
Rejected

usergmail.com
        ↓
Rejected

user@gamil.com
        ↓
Rejected

Empty Email
        ↓
Rejected

Email validation is performed before the OTP generation process begins.

OTP Test
Correct OTP
     ↓
Verification Successful

Incorrect OTP
     ↓
Error Message

Expired OTP
     ↓
OTP Rejected

Too Many Attempts
     ↓
Further Attempts Blocked
Resend OTP Test
Resend During Cooldown
        ↓
Request Blocked

Cooldown Completed
        ↓
New OTP Generated

OTP Delivered
        ↓
User Receives New Code
API Testing

The following endpoints were tested:

GET  /api/health/

GET  /api/auth/test/

POST /api/otp/send/

POST /api/otp/verify/

POST /api/otp/resend/

The complete authentication workflow was tested from email submission through OTP delivery, OTP verification, email verification, and authentication success.

🚀 Future Improvements
Password-based authentication
Password reset
Multi-factor authentication
JWT authentication
Refresh token handling
Role-based access control
User profile management
Account lockout protection
Login attempt throttling
API rate limiting
CAPTCHA integration
Authentication activity logging
Automated authentication tests
CI/CD security checks
Swagger/OpenAPI documentation
Production monitoring
Additional OAuth providers
GitHub OAuth authentication
Microsoft OAuth authentication
Advanced email existence verification
Improved authentication analytics
🎓 Educational & Portfolio Purpose

This project demonstrates practical experience with:

Django backend development
Email OTP authentication
Secure email verification
DNS and MX record validation
OTP generation and verification
OTP expiration handling
OTP attempt protection
OTP resend protection
PostgreSQL database integration
Resend email service integration
Environment-based configuration
Secure credential management
REST-style API endpoint development
Authentication testing
Production deployment
Render deployment
Git and GitHub

The project demonstrates practical understanding of secure email authentication workflows, OTP-based verification, database-backed authentication, email delivery integration, backend validation, and production-oriented Django application development.

📄 License

This project is licensed for educational and portfolio purposes.