import os

from django.db import models
from devices.models import Device

from django.contrib.auth.models import User
from django.conf import settings


class UpgradeEvent(models.Model):
    firmware_files_path = os.path.join(settings.BASE_DIR, 'upgrades', 'firmware_files')
    CODE_VERSION_CHOICES = [(f, f) for f in os.listdir(firmware_files_path)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Device)
    code_version = models.CharField(max_length=100, choices=CODE_VERSION_CHOICES)
    scheduled_upgrade = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Upgrade Event {self.pk} - {self.scheduled_upgrade}"
