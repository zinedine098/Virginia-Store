from django.urls import path
from . import views

urlpatterns = [
    path('', views.halaman_kasir, name='halaman_kasir'),
    path('tambah-ke-keranjang/', views.tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('update-jumlah/', views.update_jumlah, name='update_jumlah'),
    path('hapus-item/', views.hapus_item, name='hapus_item'),
    # path('produk/', views.produk, name='produk'),
    # path('nota-kosong/', views.nota_kosong, name='nota-kosong'),
    # path('cetak-nota-kosong/', views.cetak_nota_kosong, name='cetak-nota-kosong'),
    # path('nota-supleyer/', views.nota_supleyer, name='nota-supleyer'),
    # path('cetak-nota-supleyer/', views.cetak_nota_supleyer, name='cetak-nota-supleyer'),
]
