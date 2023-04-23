from django.db import models
from django.urls import reverse


class Device(models.Model):
    MANUFACTURER_CHOICES = [
        ('Cisco', 'Cisco'),
        ('Juniper', 'Juniper'),
        ('Huawei', 'Huawei'),
        ('Arista', 'Arista'),
    ]
    dnsName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    loginPwd = models.CharField(max_length=100)
    loginUser = models.CharField(max_length=100)
    deviceType = models.CharField(max_length=100)
    currentVersion = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=20, choices=MANUFACTURER_CHOICES, default='Cisco')

    def __str__(self):
        return self.dnsName

    def get_absolute_url(self):
        return reverse('device-detail', kwargs={'pk': self.pk})
