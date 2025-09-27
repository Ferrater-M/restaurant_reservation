from django.urls import path
from .views import auth

urlpatterns = [
    path('login/', auth.login, name='login'),  # Keep this if you want the old URL
    path('register/', auth.register, name ='register'),
    path('register_user/', auth.registerUser, name ='register_users'),
    path('login_user/', auth.loginUser, name ='register_users'),
    path('verify-email/<uuid:token>/', auth.verify_email, name='verify_email'),
    # path('request-password-reset/', auth.request_password_reset, name='request_password_reset'),
]