from django.urls import path
from . import views

app_name = 'nota_suplayer'

urlpatterns = [
    path('', views.nota_kosong, name='nota-kosong'),
    path('cetak_nota_suplayer/', views.cetak_nota_kosong, name='cetak-nota-kosong'),
    path('update_quantity_suplayer/<str:item_id>/', views.update_quantity, name='update_quantity'),
    path('delete_item/<str:item_id>/', views.delete_item, name='delete_item'),
    path('edit_dp_suplayer/<int:nota_id>/', views.edit_dp, name='edit_dp'),
    path('edit_nota_suplayer/<int:nota_id>/', views.edit_nota, name='edit_nota'),
    path('cetak_pdf_suplayer/<int:nota_id>/', views.cetak_pdf, name='cetak_pdf'),
    path('nota_palsu_suplayer/<int:nota_id>/', views.nota_palsu, name='nota_palsu'),
    path('cetak_pdf_nota_palsu_suplayer/<int:nota_id>/', views.cetak_pdf_nota_palsu, name='cetak_pdf_nota_palsu'),
    path('add_suplayer/', views.add_suplayer, name='add_suplayer'),
]