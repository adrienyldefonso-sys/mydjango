from django.urls import path

from . import views

app_name = 'semana2'

urlpatterns = [
    path('', views.objeto_list, name='objeto_list'),
    path('objeto/<int:objeto_id>/', views.objeto_detail, name='objeto_detail'),
    path('objeto/nuevo/', views.objeto_create, name='objeto_create'),
]
