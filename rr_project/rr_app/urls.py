from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # ← handles /rr/
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('getUsers/', views.getUsers, name='getUsers'),
    path('addUser/', views.addUser, name='addUsers'),
]
