from django.urls import path
from .views import UpgradeListView, UpgradeCreateView, UpgradeDetailView, UpgradeDeleteView, UpgradeUpdateView
from . import views
urlpatterns = [
    path('', UpgradeListView.as_view(), name="upgrades-home"),
    path('new/', UpgradeCreateView.as_view(), name="upgrades-create"),
    path('schedule/', views.schedule_upgrade, name='schedule_upgrade'),
    path('<int:pk>/', UpgradeDetailView.as_view(), name='upgrade-detail'),
    path('<int:pk>/update/', UpgradeUpdateView.as_view(), name="upgrade-update"),
    path('<int:pk>/delete/', UpgradeDeleteView.as_view(), name="upgrade-delete")
]
