from django.urls import path
from .views import DeviceListView, DeviceDetailView, DeviceCreateView, DeviceUpdateView, DeviceDeleteView
from . import views
app_name = 'devices'
urlpatterns = [
    path('', DeviceListView.as_view(), name="devices-home"),
    path('sort/<str:sort_by>/', DeviceListView.as_view(), name="device_home_sorted"),
    path('<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('new/', DeviceCreateView.as_view(), name="device-create"),
    path('<int:pk>/update/', DeviceUpdateView.as_view(), name="device-update"),
    path('<int:pk>/delete/', DeviceDeleteView.as_view(), name="device-delete")
]
