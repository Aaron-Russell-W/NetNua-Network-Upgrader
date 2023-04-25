from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


class Script(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Device, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
