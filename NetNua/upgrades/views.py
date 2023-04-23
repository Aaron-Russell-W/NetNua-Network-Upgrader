from datetime import datetime

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import UpgradeEventForm
from .models import UpgradeEvent
from django.contrib.auth.decorators import login_required
from . import models
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import paramiko


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
    upgrades = UpgradeEvent.objects.filter(scheduled_upgrade__lte=now, completed=False)
    for upgrade in upgrades:
        for device in upgrade.devices.all():
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(device.dnsName, username=device.loginUser, password=device.loginPwd)
            stdin, stdout, stderr = ssh.exec_command('show version')
            # handle the output
            for line in stdout:
                if 'Version' in line:
                    device.currentVersion = line.split(' ')[1]
                    device.save()
            upgrade.complated = True
            upgrade.save()
            ssh.close()
