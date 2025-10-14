from django.urls import path
from . import views

urlpatterns = [
    path('', views.nota_kosong, name='nota-kosong'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]
