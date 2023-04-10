from django import forms
from .models import UpgradeEvent


from django.forms.widgets import SelectMultiple, DateTimeInput

class UpgradeEventForm(forms.ModelForm):
    class Meta:
        model = UpgradeEvent
        fields = ['devices', 'scheduled_upgrade', 'description']
        exclude = ['user']
        widgets = {
            'devices': SelectMultiple(attrs={'multiple': True}),
            'scheduled_upgrade': DateTimeInput(attrs={'type': 'datetime-local'}),
        }