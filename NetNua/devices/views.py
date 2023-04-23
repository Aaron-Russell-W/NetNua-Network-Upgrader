import paramiko
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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


class DeviceDetailView(DetailView):
    model = Device


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm

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

    if manufacturer == 'Cisco':
        command = 'show version'
    elif manufacturer == 'Juniper':
        command = 'show version'
    elif manufacturer == 'Huawei':
        command = 'display version'
    elif manufacturer == 'Arista':
        command = 'show version'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(dnsname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        version = stdout.read().decode('utf-8')
        device.currentVersion = version
        device.save()
        return "success"
    except Exception as e:
        return str(e)