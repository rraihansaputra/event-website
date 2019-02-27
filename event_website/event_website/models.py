from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

from .validators import validate_gt_today

# Create your models here.

class AppUser(AbstractUser):
    # Custom user model to accomodate using emails as login
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()

    # validator needed to check finishing date is later than today
    finish_date = models.DateField(validators = [validate_gt_today])
    
    created_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=1000)
    created_by = models.ForeignKey(AppUser, related_name='created_event', on_delete=models.DO_NOTHING)
    users_attending = models.ManyToManyField(AppUser, related_name='events_attending')
    active = models.BooleanField(default=True)