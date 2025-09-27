from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import re, random
from ..models import VerificationCode


def send_verification_email(pending_user, request):
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': str(pending_user.token)})
    )
    
    subject = 'Verify Your Email Address'
    message = f'''
    Hi {pending_user.first_name},

    Please click the link below to verify your email:
    {verification_url}
    
    Your account role will be: {pending_user.get_role_display()}
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [pending_user.email],
        fail_silently=False,
    )


def send_verification_code_email(user):
    verification_code = f"{random.randint(0, 999999):06d}"
    VerificationCode.objects.create(
        user=user,
        code=verification_code
    )

    subject = "Your Verification Code"
    message = f"""
    Hi {user.first_name},

    Your verification code is: {verification_code}

    Enter this code to complete your verification. It will expire in 10 minutes.

    If you didn't request this, please ignore this email.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return verification_code


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