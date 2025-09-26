from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
from .models import User
import json
import logging

logger = logging.getLogger(__name__)

def login(request):
    return render(request, 'rr_app/login.html')

@csrf_exempt  # Remove this later and use proper CSRF
@require_http_methods(["POST"])
def addUser(request):
    if request.method == "POST":
        # fetching the data from the request object passed in the argument
        data = json.loads(request.body)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        date_created = datetime.now()

        # creating and appending a user object to the model
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
        # the append happens automatically
        return JsonResponse({"status" : "success", "id" : user.id})
    return JsonResponse({"status" : "error"}, status=400)

def getUsers(request):
    users = User.objects.all().values("id", "first_name", "last_name", "email", "password")
    return JsonResponse(list(users), safe=False)