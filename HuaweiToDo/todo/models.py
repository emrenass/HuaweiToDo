from datetime import datetime

from django.utils import timezone
from django.db import models

# Create your models here.

class Todo(models.Model):
    user = models.CharField(max_length=30, null=False)
    text = models.CharField(max_length=30, null=False)
    is_completed = models.BooleanField(default=False, null=False)
    created_time = models.DateTimeField(default=timezone.now, null=False)
    last_updated = models.DateTimeField(default=timezone.now, null=False)
