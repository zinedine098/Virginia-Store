from django.contrib import admin
from .models import Produk

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ('nama_barang', 'barcode', 'harga_barang', 'stok')
    search_fields = ('nama_barang', 'barcode')
    list_filter = ('harga_barang',)
