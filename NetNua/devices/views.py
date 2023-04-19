import paramiko
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
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
    fields = ['dnsName', 'location', 'deviceType', 'manufacturer', 'loginUser',
              'loginPwd']
    def form_valid(self, form):
        dnsname = form.cleaned_data.get('dnsName')
        username = form.cleaned_data.get('loginUser')
        password = form.cleaned_data.get('loginPwd')
        manufacturer = form.cleaned_data.get('manufacturer')
        if manufacturer == 'Cisco': command = 'show version'
        if manufacturer == 'Juniper': command = 'show version'
        if manufacturer == 'Arista': command = 'show version'
        if manufacturer == 'Huawei': command = 'display version'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(dnsname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        version = stdout.read().decode('utf-8')
        form.instance.currentVersion = version



class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['dnsName', 'location', 'manufacturer', 'deviceType', 'manufacturer', 'currentVersion', 'loginUser',
              'loginPwd']


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = '/'

https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md#simple-example
https://github.com/ktbyers/netmiko/blob/develop/EXAMPLES.md#auto-detection-using-ssh