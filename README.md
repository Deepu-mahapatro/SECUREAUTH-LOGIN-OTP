# SecureAuth — Email OTP Authentication System

SecureAuth is a Django-based email authentication system that verifies users using a 6-digit OTP sent to their Gmail address.

Built for **educational and portfolio purposes**.

---

## 📌 Overview

SecureAuth provides a simple email verification workflow.

Users enter their Gmail address, receive a verification OTP, and enter the OTP to verify their email.

The project uses Django, PostgreSQL, Gmail SMTP, and DNS MX-record checking.

---

## ✨ Features

- Gmail-only email validation
- Frontend and backend validation
- DNS MX-record checking
- 6-digit OTP generation
- Email OTP delivery
- OTP expiration
- OTP attempt limit
- OTP resend cooldown
- Secure OTP storage
- PostgreSQL integration
- Health-check API
- Database connectivity check
- Responsive frontend

---

## 🔐 Authentication Flow

```text
Gmail Address
     ↓
Email Validation
     ↓
Gmail & MX Check
     ↓
Generate OTP
     ↓
Send OTP
     ↓
Enter OTP
     ↓
Verify OTP
     ↓
Email Verified
     ↓
Success

| Technology   | Purpose              |
| ------------ | -------------------- |
| Python       | Programming Language |
| Django 6.1   | Backend              |
| HTML5        | Frontend             |
| CSS3         | Styling              |
| JavaScript   | Frontend Logic       |
| PostgreSQL   | Database             |
| Gmail SMTP   | OTP Delivery         |
| dnspython    | DNS MX Check         |
| Postman      | API Testing          |
| Git & GitHub | Version Control      |

EMAIL AUTH PROJECT/
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
    ├── authentication/
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

🔗 API Endpoints
Health Check
GET /api/health/

Checks whether the backend is running.

Database Test
GET /api/auth/test/

Checks the PostgreSQL connection.

Send OTP
POST /api/otp/send/

Request:

{
    "email": "user@gmail.com"
}
Verify OTP
POST /api/otp/verify/

Request:

{
    "email": "user@gmail.com",
    "otp": "123456"
}
Resend OTP
POST /api/otp/resend/

Request:

{
    "email": "user@gmail.com"
}
🛡️ Security Features
Gmail-only email validation
Frontend and backend validation
DNS MX-record checking
OTP expiration
OTP attempt limitation
OTP resend cooldown
Hashed OTP storage
Environment-based email credentials
.env excluded from Git
Safe backend error handling

MX checking confirms that a domain can receive email. It cannot confirm that a specific Gmail mailbox exists.

⚙️ Installation
1. Clone the Repository
git clone <your-repository-url>
2. Open the Backend
cd EMAIL-AUTH-PROJECT/backend
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

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

Never upload your actual .env file or Gmail App Password to GitHub.

🗄️ Database Setup

SecureAuth uses PostgreSQL.

Configure your PostgreSQL database in the Django settings/environment variables.

Then run:

python manage.py migrate
▶️ Run the Project

Start the Django server:

python manage.py runserver

Open:

http://127.0.0.1:8000/
🧪 Testing

The authentication workflow was tested using the frontend and Postman.

Tested cases include:

Valid Gmail address
Invalid email format
Non-Gmail address
Gmail domain typo
OTP generation
OTP delivery
Correct OTP
Incorrect OTP
Expired OTP
OTP attempt limit
OTP resend cooldown
Database connection
Backend health check
🚀 Future Improvements
JWT authentication
User login and logout
Password reset
IP-based rate limiting
Automated OTP cleanup
More automated tests
Production deployment
Monitoring and logging
Multi-factor authentication
🎓 Educational & Portfolio Purpose

This project demonstrates practical experience with:

Django backend development
PostgreSQL
Email authentication
OTP verification
Gmail SMTP
DNS validation
API development
Frontend and backend validation
Git and GitHub

📄 License

This project is licensed for educational and portfolio purposes.