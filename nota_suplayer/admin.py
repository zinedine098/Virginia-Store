from django.contrib import admin
from .models import NotaSuplayer

@admin.register(NotaSuplayer)
class NotaKosongAdmin(admin.ModelAdmin):
    list_display = ('kode_barang', 'nama_barang', 'jumlah_barang', 'harga')
    search_fields = ('kode_barang', 'nama_barang')
    list_filter = ('jumlah_barang',)
    ordering = ('kode_barang',)