from collections import Counter
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from devices.models import Device
from upgrades.models import UpgradeEvent
from script_manager.models import Script

@login_required
def dashboard(request):
    devices = Device.objects.all()
    manufacturers_count = Counter(device.manufacturer for device in devices)
    manufacturers_labels = list(manufacturers_count.keys())
    manufacturers_data = list(manufacturers_count.values())
    upgrades = UpgradeEvent.objects.all()
    scripts = Script.objects.all()
    print(manufacturers_count)
    print(manufacturers_labels)
    print(manufacturers_data)
    context = {
        'devices': devices,
        'upgrades': upgrades,
        'scripts': scripts,
        'manufacturer_labels_json': json.dumps(manufacturers_labels),
        'manufacturer_data_json': json.dumps(manufacturers_data),
    }

    return render(request, 'dashboard/dashboard.html', context)
