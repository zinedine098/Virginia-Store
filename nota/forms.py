from django import forms
from .models import NotaKosong, NotaPayment
from kasir.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['nama', 'alamat_customer', 'no_telpon_customer', 'shipping_agent']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pelanggan'}),
            'alamat_customer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat', 'rows': 2}),
            'no_telpon_customer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Telepon'}),
            'shipping_agent': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Agent'}),
        }

class NotaKosongForm(forms.ModelForm):
    class Meta:
        model = NotaKosong
        fields = ['kode_barang', 'nama_barang', 'deskripsi', 'jumlah_barang', 'harga', 'gambar']

        widgets = {
            'kode_barang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kode Barang'}),
            'nama_barang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Barang'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Deskripsi Barang', 'rows': 2}),
            'jumlah_barang': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'QTY'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Harga Barang'}),
            'gambar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class NotaPaymentForm(forms.ModelForm):
    class Meta:
        model = NotaPayment
        fields = ['customer', 'tanggal_sisa_bayar', 'metode_pembayaran', 'dp']

        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_sisa_bayar': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metode_pembayaran': forms.Select(attrs={'class': 'form-control'}),
            'dp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DP'}),
        }
