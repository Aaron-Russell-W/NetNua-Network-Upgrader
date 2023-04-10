from django.urls import path
from .views import DeviceListView, DeviceDetailView,DeviceCreateView,DeviceUpdateView, DeviceDeleteView
from . import views
urlpatterns= [
    path('', DeviceListView.as_view(), name="devices-home"),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('device/new/', DeviceCreateView.as_view(), name="device-create"),
    path('device/<int:pk>/update/', DeviceUpdateView.as_view(), name="device-update"),
    path('device/<int:pk>/delete/' ,DeviceDeleteView.as_view(), name="device-delete")
]