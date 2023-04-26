from django.db import models
from upgrades.models import UpgradeEvent
from script_manager.models import Script
from devices.models import Device


class Log(models.Model):
    TYPE_CHOICES = (
        ('upgrade', 'Upgrade'),
        ('script', 'Script'),
    )

    log_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    message = models.TextField()
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(UpgradeEvent, null=True, blank=True, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.log_type} - {self.timestamp}"
