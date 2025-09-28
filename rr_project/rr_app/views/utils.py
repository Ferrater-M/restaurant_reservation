# utils.py
from django.conf import settings
from django.utils import timezone
from ..models import User, UserSession
import hashlib


def sync_user_with_supabase(supabase_user):
    """
    Sync Supabase user with Django User model
    Creates or updates local user based on Supabase user data
    """
    try:
        # Extract user metadata
        user_metadata = supabase_user.user_metadata or {}
        app_metadata = supabase_user.app_metadata or {}
        
        # Get user data
        supabase_id = supabase_user.id
        email = supabase_user.email
        first_name = user_metadata.get('first_name', '')
        last_name = user_metadata.get('last_name', '')
        role = user_metadata.get('role', 'user')
        avatar_url = user_metadata.get('avatar_url', '')
        
        # Determine provider
        provider = None
        if 'providers' in app_metadata and app_metadata['providers']:
            provider = app_metadata['providers'][0]
        
        # If first/last name are empty and we have a full_name, split it
        if not first_name and not last_name and 'full_name' in user_metadata:
            full_name_parts = user_metadata['full_name'].split(' ', 1)
            first_name = full_name_parts[0]
            if len(full_name_parts) > 1:
                last_name = full_name_parts[1]
        
        # Create or update user
        user, created = User.objects.update_or_create(
            supabase_id=supabase_id,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role,
                'provider': provider,
                'avatar_url': avatar_url,
                'is_active': True
            }
        )
        
        if not created:
            # Update last login
            user.update_last_login()
        
        return user
        
    except Exception as e:
        print(f"Error syncing user with Supabase: {str(e)}")
        return None


def create_user_session(user, access_token, expires_at, request=None):
    """Create a user session record"""
    # Hash the access token for security
    token_hash = hashlib.sha256(access_token.encode()).hexdigest()
    
    # Get IP and user agent if request is provided
    ip_address = None
    user_agent = ''
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    session = UserSession.objects.create(
        user=user,
        access_token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    return session


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def cleanup_expired_sessions():
    """Clean up expired user sessions"""
    expired_sessions = UserSession.objects.filter(
        expires_at__lt=timezone.now(),
        is_active=True
    )
    expired_count = expired_sessions.count()
    expired_sessions.update(is_active=False)
    return expired_count


def validate_password_strength(password):
    """
    Validate password strength (optional - Supabase can handle this too)
    Keep this if you want additional client-side validation
    """
    min_length = 8
    max_length = 128
    
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    if len(password) > max_length:
        return False, f"Password cannot exceed {max_length} characters"
    
    # Add more validations as needed
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"
    
    return True, "Password is valid"