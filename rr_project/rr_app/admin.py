from django.contrib import admin
from .models import User, PendingUser, VerificationCode
# Register your models here.

admin.site.register(User)
admin.site.register(PendingUser)
admin.site.register(VerificationCode)