from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from logs.models import Log
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException

from .forms import ScriptForm
from .models import Script


def home(request):
    scripts = Script.objects.all()
    return render(request, 'script_manager/home.html', {'scripts': scripts})


class ScriptDetailView(DetailView):
    model = Script


class ScriptListView(ListView):
    model = Script
    template_name = 'script_manager/home.html'
    context_object_name = 'scripts'


class ScriptCreateView(LoginRequiredMixin, CreateView):
    model = Script
    form_class = ScriptForm
    success_url = "/upgrades"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ScriptUpdateView(LoginRequiredMixin, UpdateView):
    model = Script
    form_class = ScriptForm
    success_url = "/upgrades"


class ScriptDeleteView(LoginRequiredMixin, DeleteView):
    model = Script
    success_url = '/upgrades'


@login_required
def script_execute(request, pk):
    script = get_object_or_404(Script, pk=pk)
    commands = script.content.splitlines()
    user = request.user
    for device in script.devices.all():
        if device.manufacturer == 'Cisco':
            manu_type='cisco_ios'
        elif device.manufacturer == 'Juniper':
            manu_type='juniper'
        elif device.manufacturer == 'Huawei':
            manu_type='huawei'
        elif device.manufacturer == 'Arista':
            manu_type='arista_eos'
        device_data = {
            'device_type': manu_type,
            'ip': device.dnsName,
            'username': device.loginUser,
            'password': device.loginPwd,
        }

        try:
            connection = ConnectHandler(**device_data)

            for command in commands:
                try:
                    output = connection.send_command(command)
                    print(f"Command: {command}\nOutput:\n{output}\n")

                    # Create and save a Log instance
                    log = Log(
                        log_type='SUCCESS',
                        message=f"Device: {device.dnsName} Command: {command}\nOutput:\n{output}",
                        script=script,
                        user=user,
                    )
                    log.save()

                except Exception as e:
                    print(f"Error executing command '{command}' on {device.dnsName}: {e}")

                    # Create and save a Log instance
                    log = Log(
                        log_type='ERROR',
                        message=f"Error executing command '{command}': {e}",
                        script=script,
                        user=user,
                    )
                    log.save()

            # Disconnect
            connection.disconnect()

        except SSHException as e:
            print(f"SSH connection error to {device.dnsName}: {e}")

            # Create and save a Log instance
            log = Log(
                log_type='ERROR',
                message=f"SSH connection error to {device.dnsName}: {e}",
                script=script,
                user=user,
            )
            log.save()

        except Exception as e:
            print(f"Error connecting to {device.dnsName}: {e}")

            # Create and save a Log instance
            log = Log(
                log_type='ERROR',
                message=f"Error connecting to {device.dnsName}: {e}",
                script=script,
                user=user,
            )
            log.save()

    return redirect('/')