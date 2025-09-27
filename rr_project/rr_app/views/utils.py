from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import re

def send_verification_email(pending_user, request):
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': str(pending_user.token)})
    )
    
    subject = 'Verify Your Email Address'
    message = f'''
    Hi {pending_user.first_name},

    Please click the link below to verify your email:
    {verification_url}
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pending_user.email],
        fail_silently=False,
    )

def send_password_reset_email(user, request, reset_token):
    reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm', kwargs={'token': reset_token})
    )
    
    subject = 'Password Reset Request'
    message = f'''
    Hi {user.first_name},
    
    You requested a password reset. Click the link below to reset your password:
    {reset_url}
    
    If you didn't request this, please ignore this email.
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def validate_password(password):
    min_length = 8
    max_length = 20
    if not password:
        return False, "Password cannot be empty"
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    if len(password) > max_length:
        return False, f"Password cannot exceed {max_length} characters"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"
