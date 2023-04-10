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
    fields = ['dnsName', 'location', 'manufacturer', 'deviceType', 'manufacturer', 'currentVersion', 'loginUser',
              'loginPwd']


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    fields = ['dnsName', 'location', 'manufacturer', 'deviceType', 'manufacturer', 'currentVersion', 'loginUser',
              'loginPwd']


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = '/'

