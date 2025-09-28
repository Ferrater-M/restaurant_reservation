# models.py
from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    
    supabase_id = models.UUIDField(unique=True, help_text="Supabase User ID")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    date_made = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Additional fields for OAuth providers
    provider = models.CharField(max_length=50, blank=True, null=True, help_text="OAuth provider (google, azure, etc.)")
    avatar_url = models.URLField(blank=True, null=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-date_made']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class UserSession(models.Model):
    """Track user sessions for additional security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    access_token_hash = models.CharField(max_length=64)  # Store hash of access token
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.session_id}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


# Remove PendingUser and VerificationCode models since Supabase handles email verification
# Keep any other models you have for your restaurant reservation functionality