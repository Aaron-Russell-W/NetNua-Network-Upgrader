from django.urls import path
from .views import DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView
from . import views

urlpatterns = [
    path('', DeviceListView.as_view(), name="devices-home"),
    path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('new/', DeviceCreateView.as_view(), name="device-create"),
    path('<int:pk>/update/', DeviceUpdateView.as_view(), name="device-update"),
    path('<int:pk>/delete/', DeviceDeleteView.as_view(), name="device-delete")
]
