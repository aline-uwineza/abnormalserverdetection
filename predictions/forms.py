# predictions/forms.py
from django import forms
from .models import ServerActivity

class ServerActivityForm(forms.ModelForm):
    class Meta:
        model = ServerActivity
        fields = ['cpu_usage', 'memory_usage', 'disk_io', 'network_traffic', 'error_count']
        widgets = {
            'cpu_usage': forms.NumberInput(attrs={'class': 'form-control'}),
            'memory_usage': forms.NumberInput(attrs={'class': 'form-control'}),
            'disk_io': forms.NumberInput(attrs={'class': 'form-control'}),
            'network_traffic': forms.NumberInput(attrs={'class': 'form-control'}),
            'error_count': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
