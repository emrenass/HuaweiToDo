from datetime import datetime

from django.db import models

# Create your models here.

class Todo(models.Model):
    user = models.CharField(max_length=30)
    text = models.CharField(max_length=30)
    is_completed = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=datetime.now())
    last_updated = models.DateTimeField(default=datetime.now())
