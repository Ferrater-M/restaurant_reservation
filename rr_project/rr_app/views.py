from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User
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
        
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        
        user = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        
        return JsonResponse({"success": True, "id": user.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


    
def getUsers(request):
    users = User.objects.all().values("id", "first_name", "last_name", "email", "password")
    return JsonResponse(list(users), safe=False)