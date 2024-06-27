from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('metrics/', views.get_metrics, name='get_metrics'),
    path('memory_metrics/', views.get_memory_metrics, name='get_memory_metrics'),
    path('metrics2/', views.get_metrics3, name='get_metrics3'),
    path('metrics3/', views.get_metrics, name='get_metrics'),
    path('cpu_metrics/', views.get_cpu_metrics, name='cpu_metrics'),
    path('memory_metrics2/', views.get_memory_metrics, name='memory_metrics'),
    path('disk1/', views.get_disk1, name='disk_read'),
]

