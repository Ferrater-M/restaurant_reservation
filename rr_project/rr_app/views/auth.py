from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import send_verification_email, validate_password, send_verification_code_email
from ..models import User, PendingUser, VerificationCode
import json


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
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        c_password = data.get("c_password")
        role = data.get("role", "user")  # Default to user role
        
        if not first_name or not last_name or not password or not c_password:
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)

        email = data.get("email")
        if User.objects.filter(email=email).exists() or PendingUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already exists"}, status=400)

        valid, message = validate_password(password)
        if not valid:
            return JsonResponse({"success": False, "error": message}, status=400)
        
        if password != c_password:
            return JsonResponse({"success": False, "error": "Passwords do not match"}, status=400)


        pending = PendingUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role,
        )

        send_verification_email(pending, request)
        return JsonResponse({
            "success": True,
            "message": "Register successful! Please check your inbox to verify your account."
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


def verify_email(request, token):
    pending = get_object_or_404(PendingUser, token=token)

    # Create real User using Django's create_user method
    user = User.objects.create_user(
        email=pending.email,
        password=pending.password,  # Django will hash this automatically
        first_name=pending.first_name,
        last_name=pending.last_name,
        role=pending.role,
    )
    
    pending.delete()  # cleanup
    return redirect('/rr/login/')


@csrf_exempt 
@require_http_methods(["POST"])
def loginUser(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)
        
        # Use Django's authenticate function
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)  # This creates the session
            return JsonResponse({
                "success": True, 
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "is_admin": user.is_admin()
                }
            })
        else:
            # Check if user exists but is pending verification
            pending_user = PendingUser.objects.filter(email=email).first()
            if pending_user:
                return JsonResponse({"success": False, "error": "Account is pending verification"}, status=400)
            return JsonResponse({"success": False, "error": "Email or password is incorrect"}, status=400)
            
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt 
@require_http_methods(["POST"])
def logoutUser(request):
    logout(request)
    return JsonResponse({"success": True, "message": "Logged out successfully"})


@csrf_exempt 
@require_http_methods(["POST"])
def fpassRequest(request):
    try:
        data = json.loads(request.body)
        req = data.get("request")
        email = data.get("email")
        user = User.objects.filter(email=email).first()
        
        if req == "email_verif":
            if not email:
                return JsonResponse({"success": False, "error": "Please input email"}, status=400)
            if not user:
                return JsonResponse({"success": False, "error": "Email does not exist"}, status=400)
            send_verification_code_email(user)
            return JsonResponse({"success": True, "message": "Verification Code Sent"})
            
        if req == "code_verif":
            code = data.get("code")
            if not code:
                return JsonResponse({"success": False, "error": "Please input the code"}, status=400)
            code_obj = VerificationCode.objects.filter(
                user=user,
                code=code,
            ).first()   
            if not code_obj:
                return JsonResponse({"success": False, "error": "Verification code is incorrect or expired"}, status=400)
            
            if code_obj.is_expired():
                return JsonResponse({"success": False, "error": "Verification code has expired"}, status=400)
            code_obj.delete()
            return JsonResponse({"success": True, "message": "Verification is successful"})
            
        if req == "password_verif":
            password = data.get("password")
            c_password = data.get("c_password")
            if not password or not c_password:
                return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)
            valid, message = validate_password(password)
            if not valid:
               return JsonResponse({"success": False, "error": message}, status=400)
            if password != c_password:
                return JsonResponse({"success": False, "error": "Passwords do not match"}, status=400)
            
            # Use Django's set_password method to properly hash the password
            user.set_password(password)
            user.save()
            return JsonResponse({"success": True, "message": "Password has changed"})
            
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


# Role-based views
@login_required
def dashboard(request):
    if request.user.is_admin():
        return render(request, 'rr_app/admin_dashboard.html', {'user': request.user})
    else:
        return render(request, 'rr_app/user_dashboard.html', {'user': request.user})


@login_required
def admin_only_view(request):
    if not request.user.is_admin():
        return JsonResponse({"success": False, "error": "Admin access required"}, status=403)
    
    # Admin-only functionality here
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


@login_required  
def get_current_user(request):
    return JsonResponse({
        "success": True,
        "user": {
            "id": request.user.id,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "role": request.user.role,
            "is_admin": request.user.is_admin(),
            "is_authenticated": request.user.is_authenticated
        }
    })