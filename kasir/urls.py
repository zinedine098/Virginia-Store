from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.halaman_login, name='login'),
    path('logout/', views.halaman_logout, name='logout'),
    path('', views.halaman_kasir, name='halaman_kasir'),
    path('get-keranjang/', views.get_keranjang, name='get_keranjang'),
    path('tambah-ke-keranjang/', views.tambah_ke_keranjang, name='tambah_ke_keranjang'),
    path('update-jumlah/', views.update_jumlah, name='update_jumlah'),
    path('hapus-item/', views.hapus_item, name='hapus_item'),
    path('bayar/', views.halaman_bayar, name='halaman_bayar'),
    path('proses-bayar/', views.proses_bayar, name='proses_bayar'),
    path('struk/<int:transaksi_id>/', views.halaman_struk, name='halaman_struk'),
    path('batalkan-transaksi/', views.batalkan_transaksi, name='batalkan_transaksi'),
    path('get-produk-by-barcode/', views.get_produk_by_barcode, name='get_produk_by_barcode'),
    # path('produk/', views.produk, name='produk'),
    # path('nota-kosong/', views.nota_kosong, name='nota-kosong'),
    # path('cetak-nota-kosong/', views.cetak_nota_kosong, name='cetak-nota-kosong'),
    # path('nota-supleyer/', views.nota_supleyer, name='nota-supleyer'),
    # path('cetak-nota-supleyer/', views.cetak_nota_supleyer, name='cetak-nota-supleyer'),
]
