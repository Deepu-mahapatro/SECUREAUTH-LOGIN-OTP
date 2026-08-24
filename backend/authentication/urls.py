from django.urls import path
from . import views

urlpatterns = [
    # -------------------------
    # Frontend pages
    # -------------------------
    path("", views.home, name="home"),
    path("verify/", views.verify_page, name="verify-page"),
    path("success/", views.success_page, name="success-page"),

    # -------------------------
    # Backend API
    # -------------------------
    path("api/health/", views.health_check, name="health-check"),
    path("api/auth/test/", views.database_test, name="database-test"),

    path("api/otp/send/", views.send_otp, name="otp-send"),
    path("api/otp/verify/", views.verify_otp, name="otp-verify"),
    path("api/otp/resend/", views.resend_otp, name="otp-resend"),
]