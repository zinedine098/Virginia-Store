from django.urls import path
from . import views

app_name = 'nota'

urlpatterns = [
    path('', views.nota_kosong, name='nota-kosong'),
    path('cetak_nota_kosong/', views.cetak_nota_kosong, name='cetak-nota-kosong'),
    path('update_quantity/<str:item_id>/', views.update_quantity, name='update_quantity'),
    path('delete/<str:item_id>/', views.delete_item, name='delete_item'),
    path('edit_dp/<int:nota_id>/', views.edit_dp, name='edit_dp'),
    path('edit_nota/<int:nota_id>/', views.edit_nota, name='edit_nota'),
    path('cetak_pdf/<int:nota_id>/', views.cetak_pdf, name='cetak_pdf'),
    path('nota_palsu/<int:nota_id>/', views.nota_palsu, name='nota_palsu'),
    path('cetak_pdf_nota_palsu/<int:nota_id>/', views.cetak_pdf_nota_palsu, name='cetak_pdf_nota_palsu'),
    path('add_customer/', views.add_customer, name='add_customer'),
]
