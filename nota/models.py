from django.db import models

class NotaKosong(models.Model):
    kode_barang = models.CharField(max_length=50, unique=True)
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
        verbose_name = "Nota Kosong"
        verbose_name_plural = "Daftar Nota Kosong"
