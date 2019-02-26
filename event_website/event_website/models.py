from django.db import models, transaction
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    finish_date = models.DateField()
    created_time = models.DateTimeField(auto_now_add=True)
    details = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, related_name='created_event', on_delete=models.DO_NOTHING)
    users_attending = models.ManyToManyField(User, related_name='events_attending')
    active = models.BooleanField(default=True)