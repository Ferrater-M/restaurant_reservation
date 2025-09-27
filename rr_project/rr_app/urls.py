from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Keep this if you want the old URL
    path('register/', views.register, name ='register'),
    path('getUsers/', views.getUsers, name ='get_users'),
    path('addUser/', views.addUser, name ='add_users'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('getPendingUsers/', views.getPendingUsers, name='get_pending_users'),
    # path('request-password-reset/', views.request_password_reset, name='request_password_reset'),
]