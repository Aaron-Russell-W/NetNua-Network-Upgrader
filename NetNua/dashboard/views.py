from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from devices.models import Device
from upgrades.models import UpgradeEvent
from script_manager.models import Script

@login_required
def dashboard(request):
    devices = Device.objects.all()
    upgrades = UpgradeEvent.objects.all()
    scripts = Script.objects.all()

    context = {
        'devices': devices,
        'upgrades': upgrades,
        'scripts': scripts,
    }

    return render(request, 'dashboard/dashboard.html', context)
