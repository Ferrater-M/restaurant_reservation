from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Keep this if you want the old URL
    path('getUsers/', views.getUsers, name ='getUsers'),
]