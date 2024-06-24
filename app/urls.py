from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('metrics/', views.get_metrics, name='get_metrics'),
    path('memory_metrics/', views.get_memory_metrics, name='get_memory_metrics'),
    path('metrics2/', views.get_metrics3, name='get_metrics3'),
]

