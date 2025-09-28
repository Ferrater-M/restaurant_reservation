# urls.py
from django.urls import path
from .views import auth

urlpatterns = [
    # Render views
    path('login/', auth.loginRender, name='login'),
    path('register/', auth.registerRender, name='register'),
    path('forgot_password/', auth.forgot_passRender, name='forgot_password'),
    path('reset-password/', auth.reset_password_render, name='reset_password'),
    path('oauth-callback/', auth.oauth_callback, name='oauth_callback'),
    
    # API endpoints
    path('register_user/', auth.registerUser, name='register_user'),
    path('login_user/', auth.loginUser, name='login_user'),
    path('oauth-signin/', auth.signInWithOAuth, name='oauth_signin'),
    path('logout/', auth.logoutUser, name='logout'),
    path('forgot_password_request/', auth.fpassRequest, name='forgot_password_request'),
    path('update_password/', auth.updatePassword, name='update_password'),
    path('refresh_token/', auth.refreshToken, name='refresh_token'),
    
    # Protected views
    path('dashboard/', auth.dashboard, name='dashboard'),
    path('admin-dashboard/', auth.admin_only_view, name='admin_dashboard'),
    path('current-user/', auth.get_current_user, name='current_user'),
]