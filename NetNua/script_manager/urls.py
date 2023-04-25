from django.urls import path
from . import views
from .views import ScriptListView, ScriptCreateView, ScriptDetailView, ScriptDeleteView, ScriptUpdateView
app_name = 'script_manager'

urlpatterns = [
    path('', ScriptListView.as_view(), name='script_home'),
    path('new/', ScriptCreateView.as_view(), name='script_create'),
    path('update/<int:pk>/', ScriptUpdateView.as_view(), name='script_update'),
    path('delete/<int:pk>/', ScriptDeleteView.as_view(), name='script_delete'),
    path('execute/<int:pk>/', views.script_execute, name='script_execute'),
]
