# SecureAuth — Production-Level Authentication & Email Verification System

SecureAuth is a Django-based production-oriented authentication system designed to provide secure user registration, email verification, OTP-based authentication, Google OAuth 2.0 login, session management, and protected user access.

## 🌐 Live Demo

**Live Application:**

[Live Demo](https://django-google-authentication.onrender.com/)

**Source Code:**

[GitHub Repository](https://github.com/Deepu-mahapatro/SECUREAUTH-EMAIL-OTP.git)

## 📌 Overview

SecureAuth provides a complete authentication system instead of relying on a single login mechanism.

Users can register using an email address, receive a one-time verification password through email, verify the account, and continue through the authenticated workflow.

The application also supports Google OAuth 2.0 authentication.

## ✨ Features

- Secure user registration
- Email-based account verification
- One-Time Password (OTP) authentication
- OTP expiration handling
- OTP resend workflow
- Email format validation
- DNS-based domain verification
- MX record validation
- Google OAuth 2.0 authentication
- Google Sign-In integration
- OAuth authorization flow
- OAuth callback handling
- OAuth state validation
- Django session-based authentication
- Secure logout
- PostgreSQL database support
- Environment variable configuration
- `.env` credential protection
- Server-side validation
- Authentication error handling

## 🔐 Authentication Flow

```text
User
     ↓
Open Authentication Page
     ↓
Register / Login
     ↓
Email Validation
     ↓
DNS / MX Domain Validation
     ↓
Generate OTP
     ↓
Send OTP through Email
     ↓
User Enters OTP
     ↓
Verify OTP
     ↓
Create Django Session
     ↓
Authenticated User
Email OTP Flow
Browser
    │
    ▼
Django Application
    │
    ▼
Registration / Login Request
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
    ▼
Email Delivery
    │
    ▼
User Enters OTP
    │
    ▼
OTP Validation
    │
    ▼
Authentication Success
🛠️ Technology Stack
Technology	Purpose
Python	Programming Language
Django	Backend Web Framework
PostgreSQL	Production Database
Google OAuth 2.0	Third-Party Authentication
SMTP / Email Service	OTP Delivery
dnspython	DNS / MX Record Validation
python-dotenv	Environment Configuration
Django Sessions	Session Management
Postman	API Testing
Git & GitHub	Version Control
📂 Project Structure
SECUREAUTH-EMAIL-OTP/
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
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── authentication/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── ...
    │
    ├── templates/
    └── static/
🔗 API Endpoints
User Registration
POST /auth/register/

Begins the email verification workflow.

OTP Verification
POST /auth/verify-otp/

Validates the submitted one-time password.

Resend OTP
POST /auth/resend-otp/

Generates and sends a new verification OTP.

Google Login
GET /auth/google/login/

Starts the Google OAuth 2.0 authentication process.

Google OAuth Callback
GET /auth/google/callback/

Processes and validates the Google OAuth response.

Logout
GET /auth/logout/

Terminates the authenticated Django session.

🛡️ Security Features
Server-side authentication validation
Email format validation
DNS-based email domain validation
MX record verification
One-Time Password authentication
OTP expiration
OTP resend validation
Secure OAuth state validation
Google OAuth 2.0 authentication
Django session-based authentication
Session termination during logout
Environment-based secret management
.env excluded from Git
No authentication secrets hardcoded in source code
PostgreSQL configuration
HTTPS-ready deployment

Sensitive credentials should never be stored directly inside source code.

SECRET_KEY=your-secret-key
DEBUG=False

DATABASE_URL=your-production-database-url

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
⚙️ Installation
1. Clone the Repository
git clone <your-repository-url>
2. Open the Backend
cd SECUREAUTH-EMAIL-OTP/backend
3. Create Virtual Environment
python -m venv venv
4. Activate Virtual Environment

Windows PowerShell:

venv\Scripts\Activate.ps1
5. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file inside the backend directory.

SECRET_KEY=your-secret-key
DEBUG=True

DATABASE_URL=your-database-url

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True

Never upload your actual .env file or authentication credentials to GitHub.

🗄️ Database Setup

The project uses PostgreSQL as the production database.

python manage.py makemigrations

Then:

python manage.py migrate

Django creates the required database tables used by the authentication system.

▶️ Run the Project

Start the Django development server:

python manage.py runserver

Open:

http://127.0.0.1:8000/

The authentication page will be displayed.

🚀 Production Deployment

Before deployment, configure:

DEBUG=False
Production SECRET_KEY
Production DATABASE_URL
Email service credentials
Google OAuth credentials
Production OAuth redirect URI
Allowed hosts
HTTPS configuration
Secure session configuration
Secure CSRF configuration

Example:

Local Development
       ↓
Environment Configuration
       ↓
PostgreSQL Configuration
       ↓
Production Settings
       ↓
Database Migrations
       ↓
Cloud Deployment
       ↓
HTTPS Application
🧪 Testing

Tested cases include:

Application startup
Registration workflow
Email validation
DNS resolution
MX record validation
OTP generation
OTP verification
Invalid OTP handling
Expired OTP handling
OTP resend workflow
Google OAuth redirect
OAuth state validation
OAuth callback
Successful authentication
Django session creation
User logout
PostgreSQL connection
Environment configuration
Authentication error handling
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
🎓 Educational & Portfolio Purpose

This project demonstrates practical experience with:

Django backend development
Secure authentication architecture
Email OTP verification
DNS and MX record verification
Google OAuth 2.0
OAuth authorization flow
OAuth state validation
Django authentication framework
Session management
PostgreSQL database integration
Environment-based configuration
Secure credential management
Authentication testing
Production deployment
Git and GitHub

The project demonstrates practical understanding of secure authentication workflows, email verification, OAuth integration, database-backed authentication, and production-oriented Django application development.

📄 License

This project is licensed for educational and portfolio purposes.