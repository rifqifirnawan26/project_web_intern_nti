from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('metrics/', views.get_metrics, name='get_metrics'),
    path('memory_metrics/', views.get_memory_metrics, name='get_memory_metrics'),
    path('metrics2/', views.get_metrics3, name='get_metrics3'),
    path('metrics3/', views.get_metrics, name='get_metrics'),
    path('memory_metrics2/', views.get_memory_metrics, name='memory_metrics'),
    path('diskread_metrics/', views.get_diskread_metrics, name='diskread_metrics'),
    path('diskwrite_metrics/', views.get_diskwrite_metrics, name='diskwrite_metrics'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
]

