from django.urls import path
from .views import auth

urlpatterns = [
    path('login/', auth.loginRender, name='login'),  # Keep this if you want the old URL
    path('register/', auth.registerRender, name ='register'),
    path('forgot_password/', auth.forgot_passRender, name ='forgot_password'),
    path('register_user/', auth.registerUser, name ='register_user'),
    path('login_user/', auth.loginUser, name ='login_user'),
    path('fpass_request/', auth.fpassRequest, name ='fpass_request'),
    path('verify-email/<uuid:token>/', auth.verify_email, name='verify_email'),
    # path('request-password-reset/', auth.request_password_reset, name='request_password_reset'),
]