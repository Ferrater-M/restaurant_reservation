from django.urls import path
from .import views

urlpatterns = [
    path('', views.login, name='login'),  # Keep this if you want the old URL
]