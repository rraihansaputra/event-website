from django.db import models, transaction
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    finish_date = models.DateField()
    details = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, related_name='created_event', on_delete=models.DO_NOTHING)
    users_attending = models.ManyToManyField(User, related_name='users_attending')
    active = models.BooleanField(default=True)