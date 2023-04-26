from django.shortcuts import render
from devices.models import Device
from script_manager.models import Script
from upgrades.models import UpgradeEvent
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Log

@login_required
def log_list(request):
    logs = Log.objects.all().order_by('-timestamp')
    context = {
        'logs': logs,
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = Log.objects.all()
        context['device'] = Device.objects.all()
        context['script'] = Script.objects.all()
        context['upgrade'] = UpgradeEvent.objects.all()
        return context

    return render(request, 'logs/log_list.html', context)
