from django.db import models
from kasir.models import Suplayer

class NotaPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('tunai', 'Tunai'),
        ('debit', 'Debit'),
    ]

    suplayer = models.ForeignKey(Suplayer, on_delete=models.CASCADE)
    tanggal_sisa_bayar = models.DateField()
    metode_pembayaran = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    total_bayar = models.DecimalField(max_digits=12, decimal_places=2)
    dp = models.DecimalField(max_digits=12, decimal_places=2)
    sisa = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota Payment {self.id} - {self.suplayer.nama} - {self.total_bayar}"

    class Meta:
        verbose_name = "Nota Payment"
        verbose_name_plural = "Nota Payments"

class NotaSuplayer(models.Model):
    nota_payment = models.ForeignKey(NotaPayment, on_delete=models.CASCADE, related_name='items')
    kode_barang = models.CharField(max_length=50)
    nama_barang = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    jumlah_barang = models.PositiveIntegerField(default=0)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    gambar = models.ImageField(upload_to='gambar_barang/', blank=True, null=True)

    def __str__(self):
        return f"{self.kode_barang} - {self.nama_barang}"

    @property
    def subtotal(self):
        return self.harga * self.jumlah_barang

    class Meta:
        verbose_name = "Nota Suplayer"
        verbose_name_plural = "Daftar Nota Suplayer"
