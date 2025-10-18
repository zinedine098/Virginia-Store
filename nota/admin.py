from django.contrib import admin
from .models import NotaKosong, NotaPayment

@admin.register(NotaPayment)
class NotaPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'tanggal_sisa_bayar', 'metode_pembayaran', 'total_bayar', 'dp', 'sisa', 'is_temporary')
    search_fields = ('customer__nama', 'metode_pembayaran')
    list_filter = ('metode_pembayaran', 'is_temporary', 'tanggal_sisa_bayar')
    ordering = ('-created_at',)

@admin.register(NotaKosong)
class NotaKosongAdmin(admin.ModelAdmin):
    list_display = ('kode_barang', 'nama_barang', 'jumlah_barang', 'harga')
    search_fields = ('kode_barang', 'nama_barang')
    list_filter = ('jumlah_barang',)
    ordering = ('kode_barang',)

