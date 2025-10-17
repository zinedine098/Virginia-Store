from django.db import models

class Produk(models.Model):
    nama_barang = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    harga_barang = models.DecimalField(max_digits=12, decimal_places=2)
    stok = models.PositiveIntegerField()
    gambar = models.ImageField(upload_to='gambar_produk/', blank=True, null=True)

    def __str__(self):
        return self.nama_barang

class Customer(models.Model):
    nama = models.CharField(max_length=100)
    alamat_customer = models.TextField(blank=True, null=True)
    no_telpon_customer = models.CharField(max_length=20, blank=True, null=True)
    shipping_agent = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama
    
class Suplayer(models.Model):
    nama = models.CharField(max_length=100)
    alamat_suplayer = models.TextField(blank=True, null=True)
    no_telpon_suplayer = models.CharField(max_length=20, blank=True, null=True)
    shipping_agent = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nama

class Transaksi(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('transfer', 'Transfer'),
    ]

    no_transaksi = models.CharField(max_length=20, unique=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    change = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.no_transaksi


class DetailTransaksi(models.Model):
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.produk.nama_barang} x {self.jumlah}"

class InformasiToko(models.Model):
    address = models.TextField()
    factory = models.TextField()
    phone = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "Informasi Toko"

    class Meta:
        verbose_name = "Informasi Toko"
        verbose_name_plural = "Informasi Toko"
