from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User
from .utils import send_verification_email
from .models import User, PendingUser
import json


def login(request):
    return render(request, 'rr_app/login.html')

def register(request):
    return render(request, 'rr_app/register.html')

@csrf_exempt 
@require_http_methods(["POST"])
def addUser(request):
    try:
        data = json.loads(request.body)
        print("RAW BODY:", request.body) 

        email = data.get("email")
        if User.objects.filter(email=email).exists() or PendingUser.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already exists"}, status=400)
        print("1") 
        pending = PendingUser.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=email,
            password=data.get("password"),
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

# @csrf_exempt
# @require_http_methods(["POST"])
# def request_password_reset(request):
#     try:
#         data = json.loads(request.body)
#         email = data.get("email")
        
#         try:
#             user = User.objects.get(email=email)
#             reset_token = str(uuid.uuid4())
            
#             # You might want to store this token in the database
#             # For now, we'll just send it
#             send_password_reset_email(user, request, reset_token)
            
#             return JsonResponse({
#                 "success": True,
#                 "message": "If this email exists in our system, you will receive a password reset link."
#             })
#         except User.DoesNotExist:
#             # Don't reveal that the email doesn't exist for security
#             return JsonResponse({
#                 "success": True,
#                 "message": "If this email exists in our system, you will receive a password reset link."
#             })
            
#     except Exception as e:
#         return JsonResponse({"success": False, "error": "An error occurred"}, status=400)
    
def getUsers(request):
    users = User.objects.all().values("id", "first_name", "last_name", "email", "password")
    return JsonResponse(list(users), safe=False)

def getPendingUsers(request):
    users = PendingUser.objects.all().values("id", "first_name", "last_name", "email", "password")
    return JsonResponse(list(users), safe=False)