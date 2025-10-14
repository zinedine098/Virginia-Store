from django.urls import path
from . import views

app_name = 'nota'

urlpatterns = [
    path('', views.nota_kosong, name='nota-kosong'),
    path('update_quantity/<str:item_id>/', views.update_quantity, name='update_quantity'),
    path('delete/<str:item_id>/', views.delete_item, name='delete_item'),
]
