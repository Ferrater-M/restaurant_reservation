"""
URL configuration for rr_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rr_app.views import login, register, getUsers, addUser, home, dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rr/login/", login, name="login"),
    path("rr/register/", register, name="register"),
    path("rr/getUsers/", getUsers, name="getUsers"),
    path("rr/addUser/", addUser, name="addUser"),
    path("", home, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),  # ✅ FIXED
]

