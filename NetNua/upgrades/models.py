from django.db import models
from devices.models import Device

from django.contrib.auth.models import User


class UpgradeEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    devices = models.ManyToManyField(Device)
    scheduled_upgrade = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Upgrade Event {self.pk} - {self.scheduled_upgrade}"
