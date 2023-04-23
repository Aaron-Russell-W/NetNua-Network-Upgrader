from django.contrib import messages
import paramiko
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

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
def script_execute(request, script_id):
    script = get_object_or_404(Script, id=script_id, user=request.user)
    devices = script.devices.all()

    # Your logic to execute the script on the selected devices
    # This can be done through SSH, API calls, or other methods depending on the devices
    for device in devices:
        # Execute script on device
        ssh = paramiko.SSHClient()

    messages.success(request, f'Script "{script.name}" has been executed on the selected devices.')
    return redirect('script_manager:script_list')
