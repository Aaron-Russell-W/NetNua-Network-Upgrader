import os

from django import forms
from .models import UpgradeEvent


from django.forms.widgets import SelectMultiple, DateTimeInput
from django.conf import settings
def get_code_versions():
    upgrade_dir = os.path.join(settings.BASE_DIR, 'upgrades','firmware_files')
    file_list = [f for f in os.listdir(upgrade_dir) if os.path.isfile(os.path.join(upgrade_dir, f))]
    return [(f, f) for f in file_list]
class UpgradeEventForm(forms.ModelForm):
    code_version=forms.ChoiceField(choices=get_code_versions())
    class Meta:
        model = UpgradeEvent
        fields = ['devices','code_version', 'scheduled_upgrade', 'description']
        exclude = ['user']
        widgets = {
            'devices': SelectMultiple(attrs={'multiple': True, 'class' : 'form-control'}),
            'scheduled_upgrade': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class' : 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class' : 'form-control'}),

        }
