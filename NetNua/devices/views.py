import paramiko
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from logs.models import Log
from .forms import DeviceForm
from .models import Device
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    context = {
        'devices': Device.objects.all()
    }
    return render(request, 'devices/home.html', context)


class DeviceListView(ListView):
    model = Device
    template_name = 'devices/home.html'
    context_object_name = 'devices'
    def get_queryset(self):
        sort_by = self.kwargs.get('sort_by')
        if sort_by == 'manufacturer':
            return Device.objects.order_by('manufacturer')
        elif sort_by == 'deviceType':
            return Device.objects.order_by('deviceType')
        elif sort_by == 'location':
            return Device.objects.order_by('location')
        elif sort_by == 'currentVersion':
            return Device.objects.order_by('currentVersion')
        else:
            return Device.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.kwargs.get('sort_by')
        return context

class DeviceDetailView(DetailView):
    model = Device


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    success_url = "/"
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        result = update_device_version(self.object)
        if result == "success":
            messages.success(self.request, "Device created successfully and version information updated.")
        else:
            messages.error(self.request, f"Device created, but failed to update version information: {result}")
        return response


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['dnsName', 'location', 'manufacturer', 'deviceType', 'manufacturer', 'currentVersion', 'loginUser',
              'loginPwd']
    success_url = "/"


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = '/'


def update_device_version(device):
    dnsname = device.dnsName
    username = device.loginUser
    password = device.loginPwd
    manufacturer = device.manufacturer

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if manufacturer == 'Cisco':
        try:
            ssh.connect(dnsname, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command("show version")
            output = stdout.readlines()
            output = output[0].split(",")
            version = output[2].replace('Version', '').strip()
            print(version)
            device.currentVersion = version
            device.save()
            create_log_entry(f"Version updated to {version}", "INFO", device)
            return "success"
        except Exception as e:
            create_log_entry(f"Failed to update version: {e}", "ERROR", device)
            return str(e)
    elif manufacturer == 'Arista':
        try:
        # Automatically add SSH keys from servers
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the server
            ssh.connect(dnsname, username=username, password=password)
        # Run the command to get the version from the Cisco device
            stdin, stdout, stderr = ssh.exec_command("show version")
        # Get the output from the executed command
            output = stdout.readlines()
            version = output[5].replace('Software image version:', '').strip()
            device.currentVersion = version
            device.save()
            return "success"
        except Exception as e:
            return str(e)
def create_log_entry(message,log_level,device):
    log_entry = Log.objects.create(
        message=message,
        log_type=log_level,
        device=device
    )
    log_entry.save()
