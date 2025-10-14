from django.urls import path
from . import views

urlpatterns = [
    path('', views.nota_kosong, name='nota-kosong'),
]