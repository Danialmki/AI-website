# models.py
from django.db import models
from django.contrib.auth.models import User
import random

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.verification_code:
            # Generate a random 6-digit number
            self.verification_code = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"EmailVerification for {self.user.username}"
