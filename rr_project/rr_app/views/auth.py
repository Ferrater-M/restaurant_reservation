from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import User
from ..utils import send_verification_email
from ..models import User, PendingUser
from django.contrib.auth.hashers import make_password, check_password
import json


def login(request):
    return render(request, 'rr_app/login.html')

def register(request):
    return render(request, 'rr_app/register.html')

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
            "message": "Please verify your email before logging in."
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
                return JsonResponse({"success": True, "message": "Login successfull"})
            else:
                return JsonResponse({"success": False, "error": "Password is incorrect"}, status=400)
        else:
            pending_user = PendingUser.objects.filter(email=email).first()
            if pending_user and check_password(password, pending_user.password):
                return JsonResponse({"success": False, "error": "Account is pending verification"}, status=400)
            return JsonResponse({"success": False, "error": "Email is not registerd"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)