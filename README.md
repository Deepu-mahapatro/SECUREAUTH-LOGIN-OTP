SecureAuth — Email OTP Authentication System

SecureAuth is a Django-based authentication system that allows users to securely authenticate using their email address and a one-time password (OTP).

The project implements a complete email authentication workflow, including email submission, secure OTP generation, OTP delivery through the Resend email API, OTP expiration, attempt limitation, resend cooldown, database storage, OTP verification, and successful authentication.

Built for educational and portfolio purposes.

🌐 Live Demo

Live Application:

https://secureauth-login-otp.onrender.com

Source Code:

SecureAuth GitHub Repository

📌 Overview

SecureAuth provides a simple and secure email-based authentication workflow.

Users start the authentication process by entering their email address into the application. Django validates the email address and generates a secure six-digit OTP.

The generated OTP is sent to the user's email through the Resend email API.

The OTP is stored in the PostgreSQL database together with its expiration and validation information.

The user then enters the received OTP. Django validates the OTP, checks its expiration and attempt limits, and completes the authentication process when the submitted code is correct.

The project uses Django, PostgreSQL, Resend, JavaScript, environment-based configuration, and secure OTP validation mechanisms.

✨ Features
Email-based authentication
Six-digit OTP generation
OTP email delivery using Resend
OTP verification
OTP expiration
Maximum OTP attempt limitation
OTP resend cooldown
PostgreSQL database
Django backend
Responsive authentication interface
JavaScript-based form handling
Backend API endpoints
Email validation
Authentication success handling
Authentication error handling
Environment variable configuration
Secure credential management
.env credential protection
Production deployment using Render
Gunicorn production server
WhiteNoise static file serving
Local PostgreSQL development support
Production PostgreSQL support
Session-based authentication
Secure OTP processing
🔐 Authentication Flow
User
     ↓
Open SecureAuth Authentication Page
     ↓
Enter Email Address
     ↓
Submit Email
     ↓
Django OTP API
     ↓
Validate Email
     ↓
Generate 6-Digit OTP
     ↓
Check OTP Rules
     ↓
Send OTP Through Resend
     ↓
Store OTP in PostgreSQL
     ↓
User Receives Email
     ↓
Enter OTP
     ↓
Django OTP Verification API
     ↓
Validate OTP
     ↓
Check Expiration
     ↓
Check Attempt Limit
     ↓
Authentication Success
Email OTP Flow
Browser
    │
    ▼
Django Application
    │
    ▼
/api/otp/send/
    │
    ▼
Email Validation
    │
    ▼
Generate OTP
    │
    ▼
Resend Email API
    │
    ▼
User Email Inbox
    │
    ▼
User Enters OTP
    │
    ▼
/api/otp/verify/
    │
    ▼
OTP Validation
    │
    ▼
Authentication Success

The authentication process starts when the user enters an email address.

Django receives the request through the OTP send endpoint and validates the submitted email address.

A six-digit OTP is generated and sent to the user's email using Resend.

The OTP information is stored in PostgreSQL.

The user enters the received verification code.

Django checks whether the OTP is correct, whether it has expired, and whether the maximum number of attempts has been exceeded.

If validation succeeds, the user is authenticated successfully.

🛠️ Technology Stack
Technology	Purpose
Python	Programming Language
Django 6.1	Backend Web Framework
HTML5	Frontend
CSS3	Styling
JavaScript	Frontend Logic
PostgreSQL	Database
Resend	OTP Email Delivery
python-dotenv	Environment Configuration
dj-database-url	Database URL Configuration
WhiteNoise	Static File Serving
Gunicorn	Production WSGI Server
Git & GitHub	Version Control
Render	Production Deployment
📂 Project Structure
SECUREAUTH-EMAIL-OTP/
│
├── README.md
├── .gitignore
│
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── .env
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
    │   ├── utils.py
    │   ├── email_service.py
    │   ├── urls.py
    │   └── ...
    │
    ├── templates/
    │   └── ...
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       └── script.js
    │
    └── staticfiles/

The project is organized into a Django backend, authentication application, templates, static files, and configuration files.

The authentication application contains the OTP generation, verification, database operations, and email delivery logic.

The .env file is used for local sensitive configuration and must not be uploaded to GitHub.

🔗 API Endpoints
Send OTP
POST /api/otp/send/

Starts the email authentication process.

The endpoint:

Receives the user's email address.
Validates the email.
Checks OTP restrictions.
Generates a six-digit OTP.
Sends the OTP using Resend.
Stores the OTP information in PostgreSQL.
Verify OTP
POST /api/otp/verify/

Verifies the OTP submitted by the user.

The endpoint validates:

Submitted email.
OTP value.
OTP expiration.
Maximum verification attempts.
OTP validity.

If the OTP is correct and valid, authentication is completed.

Authentication Page
GET /

Displays the SecureAuth authentication interface where the user enters their email address.

🛡️ Security Features
Six-digit OTP authentication
OTP expiration
Maximum OTP attempt limitation
OTP resend cooldown
Server-side OTP validation
PostgreSQL-backed OTP storage
Resend API email delivery
Environment-based credential management
.env excluded from Git
API key protection
Database credential protection
Backend authentication processing
Email validation
Authentication error handling
Secure session management
Production HTTPS through Render
No sensitive credentials hardcoded in source code

The project uses environment variables for sensitive configuration.

Example:

RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=onboarding@resend.dev
SECRET_KEY=your-secret-key
DATABASE_URL=your-production-database-url

For local PostgreSQL development:

DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

The actual .env file must never be uploaded to GitHub.

⚙️ Installation
1. Clone the Repository
git clone https://github.com/Deepu-mahapatro/SECUREAUTH-EMAIL-OTP.git
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

For local development:

DEBUG=True

DB_NAME=email_auth_db
DB_USER=postgres
DB_PASSWORD=your-postgresql-password
DB_HOST=localhost
DB_PORT=5432

OTP_EXPIRY_MINUTES=5
OTP_MAX_ATTEMPTS=5
OTP_RESEND_COOLDOWN_SECONDS=60

RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=onboarding@resend.dev

SECRET_KEY=your-development-secret-key

For production, Render provides the PostgreSQL DATABASE_URL.

Production environment variables include:

DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-render-postgresql-url
RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=onboarding@resend.dev

Sensitive credentials must never be committed to GitHub.

🗄️ Database Setup

The project uses PostgreSQL as its database.

Local Development

The local application connects to PostgreSQL using:

HOST=localhost
PORT=5432

After configuring PostgreSQL and the environment variables, run:

python manage.py makemigrations

Then:

python manage.py migrate

Django creates the required database tables used by the authentication system, OTP records, sessions, and other application components.

Production

The deployed application uses PostgreSQL through the Render-provided:

DATABASE_URL

The Django settings support both local PostgreSQL configuration and production PostgreSQL configuration.

▶️ Run the Project

Start the Django development server:

python manage.py runserver

Open:

http://127.0.0.1:8000/

The SecureAuth authentication page will be displayed.

Enter an email address and submit the form.

The application sends the OTP through Resend.

The user then enters the received OTP to complete authentication.

🧪 Testing

The SecureAuth authentication workflow was tested using the browser, Django development server, PostgreSQL database, Resend email API, and production deployment environment.

Tested cases include:

Application startup
Authentication page
Email input
Email validation
OTP generation
OTP email delivery
Resend API integration
PostgreSQL connection
OTP database storage
OTP verification
Correct OTP handling
Incorrect OTP handling
Expired OTP handling
Maximum OTP attempt handling
OTP resend cooldown
Authentication success
Authentication error handling
Environment variable configuration
Production database configuration
Production email configuration
Render deployment
Static file serving
Browser-based testing
Browser Authentication Test

The main authentication workflow was tested using:

http://127.0.0.1:8000/

Production testing was performed using:

https://secureauth-login-otp.onrender.com

OTP request:

POST /api/otp/send/

OTP verification:

POST /api/otp/verify/

The complete authentication flow was tested from email submission through OTP delivery and OTP verification.

🚀 Future Improvements
Password-based authentication
Password reset
Multi-factor authentication
JWT authentication
Role-based access control
User profile management
Additional authentication providers
Google OAuth authentication
GitHub OAuth authentication
Microsoft OAuth authentication
Automated authentication tests
API documentation using Swagger/OpenAPI
Advanced rate limiting
Authentication activity tracking
Email delivery monitoring
Authentication audit logs
Advanced account security controls
Custom verified email domain
Production monitoring and alerting
🎓 Educational & Portfolio Purpose

This project demonstrates practical experience with:

Django backend development
Email-based authentication
OTP generation
OTP verification
Transactional email API integration
Resend API
PostgreSQL database management
Database-backed authentication
API endpoint development
Session management
Environment-based configuration
Secure credential management
Backend development
Frontend JavaScript integration
Authentication testing
Production deployment
Render deployment
Static file management
Git and GitHub

The project is designed to demonstrate practical understanding of modern email authentication workflows, OTP security, database integration, and secure Django application deployment.

📄 License

This project is licensed for educational and portfolio purposes.