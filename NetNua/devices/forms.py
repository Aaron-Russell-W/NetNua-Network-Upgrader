from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['dnsName','manufacturer','deviceType','location', 'loginUser', 'loginPwd']
