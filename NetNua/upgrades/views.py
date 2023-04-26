import os
import time
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from netmiko import ConnectHandler, file_transfer, progress_bar

from .forms import UpgradeEventForm
from .models import UpgradeEvent


def home(request):
    upgrades = UpgradeEvent.objects.all()
    return render(request, 'upgrades/home.html', {'upgrades': upgrades})


class UpgradeDetailView(DetailView):
    model = UpgradeEvent


class UpgradeListView(ListView):
    model = UpgradeEvent
    template_name = 'upgrades/home.html'
    context_object_name = 'upgrades'


class UpgradeCreateView(LoginRequiredMixin, CreateView):
    model = UpgradeEvent
    form_class = UpgradeEventForm
    success_url = "/upgrades"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpgradeUpdateView(LoginRequiredMixin, UpdateView):
    model = UpgradeEvent
    form_class = UpgradeEventForm
    success_url = "/upgrades"


class UpgradeDeleteView(LoginRequiredMixin, DeleteView):
    model = UpgradeEvent
    success_url = '/upgrades'


@login_required
def schedule_upgrade(request):
    if request.method == 'POST':
        form = UpgradeEventForm(request.POST)
        if form.is_valid():
            upgrade_event = form.save(commit=False)
            upgrade_event.user = request.user
            upgrade_event.save()
            form.save_m2m()  # Save many-to-many relationships
            form = UpgradeEventForm()  # Reset the form
    else:
        form = UpgradeEventForm()

    return render(request, 'upgrades/schedule_upgrade.html', {'form': form})


def check_upgrades(request):
    now = datetime.now()
    upgrades = UpgradeEvent.objects.all().filter(scheduled_upgrade__lte=now, completed=False)
    for upgrade in upgrades:
        if scp_file(upgrade):
            print("All devices have been upgraded. Verifying Connection")
            for device in upgrade.devices.all():
                print(f"Verifying Connection to {device.dnsName}")
                if wait_for_connection(device):
                    print(f"Connection to {device.dnsName} verified")
                    device.currentVersion = upgrade.code_version
                else:
                    print(f"Connection to {device.dnsName} failed")


def scp_file(upgrade):
    for device in upgrade.devices.all():
        if device.manufacturer == 'Arista':
            device_type = 'arista_eos'
            device_location = '/mnt/flash'
        elif device.manufacturer == 'Cisco':
            device_type = 'cisco_ios'
            device_location = 'flash:'
        elif device.manufacturer == 'Juniper':
            device_type = 'juniper_junos'
            device_location = 'var/home/netnua'
        device = {
            "device_type": device_type,
            "ip": device.dnsName,
            "username": device.loginUser,
            "password": device.loginPwd,
            "session_log": "my_session.log",
        }
        source_file = os.path.join(settings.BASE_DIR, 'upgrades', 'firmware_files', upgrade.code_version)
        file_system = device_location
        dest_file = upgrade.code_version
        ssh_conn = ConnectHandler(**device)
        ssh_conn.enable()
        transfer_dict = file_transfer(
            ssh_conn,
            source_file=source_file,
            dest_file=dest_file,
            file_system=file_system,
            direction="put",
            overwrite_file=True,
            progress4=progress_bar,
        )
        print(transfer_dict)
        print(f"Successfully transferred file to {{device}}")
        boot_system_cmd = f"boot system flash:{dest_file}"
        ssh_conn.send_command(boot_system_cmd)
        ssh_conn.send_command("write memory")
        ssh_conn.send_command("copy running-config startup-config")
        ssh_conn.send_command("reload in 5")
        ssh_conn.disconnect()

    return True


def wait_for_connection(device, max_retries=10, retry_interval=30):
    retries = 0
    while retries < max_retries:
        is_connected = verify_device_connection(device)
        if is_connected:
            return True
        else:
            time.sleep(retry_interval)
            retries += 1
    return False


def verify_device_connection(device):
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("show version")
        connection.disconnect()

        # Check for specific keywords in the output to ensure you are connected to the correct device
        if "Arista" in output:
            return True
        else:
            return False
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
