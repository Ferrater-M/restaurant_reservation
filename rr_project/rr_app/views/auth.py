from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import send_verification_email, validate_password, send_verification_code_email
from ..models import User, PendingUser, VerificationCode
from django.contrib.auth.hashers import make_password, check_password
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
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        password=data.get("password")
        c_password=data.get("c_password")
        
        if(not first_name or not last_name or not password or not c_password):
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)

        email = data.get("email")
        if User.objects.filter(email=email).exists() or PendingUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already exists"}, status=400)

        valid, message = validate_password(password)
        if(not valid):
            return JsonResponse({"success": False, "error": message}, status=400)
        
        if(password != c_password):
            return JsonResponse({"success": False, "error": "Passwords do not match"}, status=400)


        hashed_password = make_password(password)

        pending = PendingUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
        )

        send_verification_email(pending, request)
        print("2") 
        return JsonResponse({
            "success": True,
            "message": "Register successful! Please check your inbox to verify your account."
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)



def verify_email(request, token):
    pending = get_object_or_404(PendingUser, token=token)

    # Create real User
    user = User.objects.create(
        first_name=pending.first_name,
        last_name=pending.last_name,
        email=pending.email,
        password=pending.password
    )
    pending.delete()  # cleanup

    # Auto-login or redirect
    return redirect('/rr/login/')

@csrf_exempt 
@require_http_methods(["POST"])
def loginUser(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        if(not email or not password):
            return JsonResponse({"success": False, "error": "Please input all fields"}, status=400)
        
        user = User.objects.filter(email=email).first()
        if user:
            if check_password(password, user.password):
                return JsonResponse({"success": True, "message": "Login is successfull"})
            else:
                return JsonResponse({"success": False, "error": "Email or password is incorrect"}, status=400)
        else:
            pending_user = PendingUser.objects.filter(email=email).first()
            if pending_user and check_password(password, pending_user.password):
                return JsonResponse({"success": False, "error": "Account is pending verification"}, status=400)
            return JsonResponse({"success": False, "error": "Email or password is incorrect"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

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
            if(not valid):
               return JsonResponse({"success": False, "error": message}, status=400)
            if password != c_password:
                return JsonResponse({"success": False, "error": "Passwords do not match"}, status=400)
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()
            return JsonResponse({"success": True, "message": "Password has changed"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

def confirmPass(request):
    return JsonResponse
    
