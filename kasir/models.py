from django.db import models

class Produk(models.Model):
    nama_barang = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    harga_barang = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.PositiveIntegerField()
    gambar = models.ImageField(upload_to='gambar_produk/', blank=True, null=True)

    def __str__(self):
        return self.nama_barang

class Transaksi(models.Model):
    no_transaksi = models.CharField(max_length=20, unique=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.no_transaksi


class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.produk.nama_barang} x {self.jumlah}"