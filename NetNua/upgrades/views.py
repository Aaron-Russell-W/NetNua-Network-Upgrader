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
