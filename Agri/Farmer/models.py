import pyotp
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# models.py
import pyotp
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    otp_secret = models.CharField(max_length=16, default=pyotp.random_base32)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()  # Generate a new OTP secret
        super().save(*args, **kwargs)
        
    def generate_otp(self):
            # Generate a TOTP object and get the current OTP
            totp = pyotp.TOTP(self.otp_secret)
            return totp.now()

    def __str__(self):
            return f"{self.user.username} Profile"
