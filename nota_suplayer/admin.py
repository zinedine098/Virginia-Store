from django.contrib import admin
from .models import NotaSuplayer, NotaPayment

@admin.register(NotaPayment)
class NotaPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'suplayer', 'tanggal_sisa_bayar', 'metode_pembayaran', 'total_bayar', 'dp', 'sisa', 'is_temporary')
    search_fields = ('suplayer__nama', 'metode_pembayaran')
    list_filter = ('metode_pembayaran', 'is_temporary', 'tanggal_sisa_bayar')
    ordering = ('-created_at',)

@admin.register(NotaSuplayer)
class NotaKosongAdmin(admin.ModelAdmin):
    list_display = ('kode_barang', 'nama_barang', 'jumlah_barang', 'harga')
    search_fields = ('kode_barang', 'nama_barang')
    list_filter = ('jumlah_barang',)
    ordering = ('kode_barang',)
