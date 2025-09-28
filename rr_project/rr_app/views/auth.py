# views/auth.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from supabase import create_client, Client
from ..models import User
from .utils import sync_user_with_supabase
import json
import jwt
from functools import wraps


# Initialize Supabase client
def get_supabase_client():
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


def supabase_auth_required(view_func):
    """Decorator to require Supabase authentication"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"success": False, "error": "Authentication required"}, status=401)
        
        token = auth_header.split('Bearer ')[1]
        supabase = get_supabase_client()
        
        try:
            # Verify the token with Supabase
            user_response = supabase.auth.get_user(token)
            if user_response.user:
                # Sync user with local Django model
                django_user = sync_user_with_supabase(user_response.user)
                request.user = django_user
                request.supabase_user = user_response.user
                return view_func(request, *args, **kwargs)
        except Exception as e:
            pass
        
        return JsonResponse({"success": False, "error": "Invalid token"}, status=401)
    
    return wrapper


def loginRender(request):
    return render(request, 'rr_app/login.html')


def registerRender(request):
    return render(request, 'rr_app/register.html')


def forgot_passRender(request):
    return render(request, 'rr_app/fpass.html')


@csrf_exempt 
@require_http_methods(["POST"])
def registerUser(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        
        if not all([email, password, first_name, last_name]):
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)

        supabase = get_supabase_client()
        
        # Register with Supabase
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": data.get("role", "user")
                }
            }
        })
        
        if auth_response.user:
            return JsonResponse({
                "success": True,
                "message": "Registration successful! Please check your email to verify your account.",
                "user": {
                    "id": auth_response.user.id,
                    "email": auth_response.user.email
                }
            })
        else:
            return JsonResponse({"success": False, "error": "Registration failed"}, status=400)
            
    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message:
            return JsonResponse({"success": False, "error": "Email already exists"}, status=400)
        return JsonResponse({"success": False, "error": error_message}, status=400)


@csrf_exempt 
@require_http_methods(["POST"])
def loginUser(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)
        
        supabase = get_supabase_client()
        
        # Sign in with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if auth_response.user and auth_response.session:
            # Sync user with Django model
            django_user = sync_user_with_supabase(auth_response.user)
            
            return JsonResponse({
                "success": True,
                "message": "Login successful",
                "session": {
                    "access_token": auth_response.session.access_token,
                    "refresh_token": auth_response.session.refresh_token,
                    "expires_at": auth_response.session.expires_at
                },
                "user": {
                    "id": django_user.id,
                    "supabase_id": django_user.supabase_id,
                    "email": django_user.email,
                    "first_name": django_user.first_name,
                    "last_name": django_user.last_name,
                    "role": django_user.role,
                    "is_admin": django_user.is_admin()
                }
            })
        else:
            return JsonResponse({"success": False, "error": "Invalid credentials"}, status=400)
            
    except Exception as e:
        error_message = str(e)
        if "Invalid login credentials" in error_message:
            return JsonResponse({"success": False, "error": "Email or password is incorrect"}, status=400)
        elif "Email not confirmed" in error_message:
            return JsonResponse({"success": False, "error": "Please verify your email first"}, status=400)
        return JsonResponse({"success": False, "error": error_message}, status=400)


@csrf_exempt 
@require_http_methods(["POST"])
def signInWithOAuth(request):
    try:
        data = json.loads(request.body)
        provider = data.get("provider")  # 'google' or 'azure'
        
        if provider not in ['google', 'azure']:
            return JsonResponse({"success": False, "error": "Invalid provider"}, status=400)
        
        supabase = get_supabase_client()
        
        # Get the OAuth URL
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": provider,
            "options": {
                "redirect_to": f"{request.build_absolute_uri('/')[:-1]}/rr/oauth-callback/"
            }
        })
        
        return JsonResponse({
            "success": True,
            "oauth_url": auth_response.url
        })
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


def oauth_callback(request):
    """Handle OAuth callback from Supabase"""
    try:
        # Get the session from URL fragments (handled by frontend)
        return render(request, 'rr_app/oauth_callback.html')
    except Exception as e:
        return redirect('/rr/login/?error=oauth_failed')


@csrf_exempt 
@require_http_methods(["POST"])
def logoutUser(request):
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]
            supabase = get_supabase_client()
            supabase.auth.sign_out()
        
        return JsonResponse({"success": True, "message": "Logged out successfully"})
    except Exception as e:
        return JsonResponse({"success": True, "message": "Logged out successfully"})


@csrf_exempt 
@require_http_methods(["POST"])
def fpassRequest(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        
        if not email:
            return JsonResponse({"success": False, "error": "Please input email"}, status=400)
        
        supabase = get_supabase_client()
        
        # Send password reset email
        supabase.auth.reset_password_email(
            email,
            {
                "redirect_to": f"{request.build_absolute_uri('/')[:-1]}/rr/reset-password/"
            }
        )
        
        return JsonResponse({
            "success": True,
            "message": "Password reset email sent. Please check your inbox."
        })
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


def reset_password_render(request):
    """Render password reset page"""
    return render(request, 'rr_app/reset_password.html')


@csrf_exempt 
@require_http_methods(["POST"])
def updatePassword(request):
    try:
        data = json.loads(request.body)
        access_token = data.get("access_token")
        new_password = data.get("new_password")
        
        if not access_token or not new_password:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)
        
        supabase = get_supabase_client()
        
        # Update password
        supabase.auth.update_user({
            "password": new_password
        }, access_token)
        
        return JsonResponse({
            "success": True,
            "message": "Password updated successfully"
        })
        
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@supabase_auth_required
def dashboard(request):
    if request.user.is_admin():
        return render(request, 'rr_app/admin_dashboard.html', {'user': request.user})
    else:
        return render(request, 'rr_app/user_dashboard.html', {'user': request.user})


@supabase_auth_required
def admin_only_view(request):
    if not request.user.is_admin():
        return JsonResponse({"success": False, "error": "Admin access required"}, status=403)
    
    users = User.objects.all()
    users_data = [{
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        'date_made': user.date_made.strftime('%Y-%m-%d')
    } for user in users]
    
    return JsonResponse({"success": True, "users": users_data})


@supabase_auth_required  
def get_current_user(request):
    return JsonResponse({
        "success": True,
        "user": {
            "id": request.user.id,
            "supabase_id": request.user.supabase_id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": request.user.role,
            "is_admin": request.user.is_admin(),
        }
    })


@csrf_exempt 
@require_http_methods(["POST"])
def refreshToken(request):
    try:
        data = json.loads(request.body)
        refresh_token = data.get("refresh_token")
        
        if not refresh_token:
            return JsonResponse({"success": False, "error": "Refresh token required"}, status=400)
        
        supabase = get_supabase_client()
        
        # Refresh the session
        auth_response = supabase.auth.refresh_session(refresh_token)
        
        if auth_response.session:
            return JsonResponse({
                "success": True,
                "session": {
                    "access_token": auth_response.session.access_token,
                    "refresh_token": auth_response.session.refresh_token,
                    "expires_at": auth_response.session.expires_at
                }
            })
        else:
            return JsonResponse({"success": False, "error": "Failed to refresh token"}, status=400)
            
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)