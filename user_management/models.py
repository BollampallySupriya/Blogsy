from django.contrib.auth.models import AbstractUser
from django.db import models

# User Management Models

class User(AbstractUser):
    USER_STATUS_CHOICES = (('ACTIVE', 'ACTIVE'), ('SUSPENDED', 'SUSPENDED'), ('BANNED', 'BANNED'))
    country_code = models.CharField(max_length=10, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='ACTIVE') 
    is_public = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'


class Followers(models.Model):
    FOLLOWER_STATUS_CHOICES = (('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('REJECTED', ('REJECTED')))
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FOLLOWER_STATUS_CHOICES)
    requested_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'followers'

