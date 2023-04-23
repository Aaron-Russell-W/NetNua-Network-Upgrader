from django import forms
from .models import Script
from django import forms

class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['name', 'description', 'content', 'devices']
        widgets = {
            'devices': forms.SelectMultiple(attrs={'multiple': True, 'class' : 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class' : 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 20, 'cols': 40, 'class' : 'form-control'}),
        }
