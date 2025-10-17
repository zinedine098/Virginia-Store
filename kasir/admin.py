from django.contrib import admin
from .models import Produk, Customer, Transaksi, DetailTransaksi, InformasiToko, Suplayer

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('nama_barang', 'barcode', 'harga_barang', 'stok')
    search_fields = ('nama_barang', 'barcode')
    list_filter = ('harga_barang',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat_customer', 'no_telpon_customer', 'shipping_agent')
    search_fields = ('nama', 'no_telpon_customer')
    list_filter = ('shipping_agent',)

@admin.register(Suplayer)
class SuplayerAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat_suplayer', 'no_telpon_suplayer', 'shipping_agent')
    search_fields = ('nama', 'no_telpon_suplayer')
    list_filter = ('shipping_agent',)

@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ('no_transaksi', 'tanggal', 'customer', 'payment_method', 'amount_paid', 'change')
    search_fields = ('no_transaksi', 'customer__nama')
    list_filter = ('payment_method', 'tanggal')

@admin.register(DetailTransaksi)
class DetailTransaksiAdmin(admin.ModelAdmin):
    list_display = ('transaksi', 'produk', 'jumlah', 'subtotal')
    search_fields = ('transaksi__no_transaksi', 'produk__nama_barang')
    list_filter = ('produk',)

@admin.register(InformasiToko)
class InformasiTokoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email')
    search_fields = ('address', 'email')
