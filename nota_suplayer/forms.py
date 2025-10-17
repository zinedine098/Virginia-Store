from django import forms
from .models import NotaSuplayer, NotaPayment
from kasir.models import Suplayer

class SuplayerForm(forms.ModelForm):
    class Meta:
        model = Suplayer
        fields = ['nama', 'alamat_suplayer', 'no_telpon_suplayer', 'shipping_agent']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Suplayer'}),
            'alamat_suplayer': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat', 'rows': 2}),
            'no_telpon_suplayer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Telepon'}),
            'shipping_agent': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping Agent'}),
        }

class NotaKosongForm(forms.ModelForm):
    class Meta:
        model = NotaSuplayer
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
        fields = ['suplayer', 'tanggal_sisa_bayar', 'metode_pembayaran', 'dp']

        widgets = {
            'suplayer': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_sisa_bayar': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'metode_pembayaran': forms.Select(attrs={'class': 'form-control'}),
            'dp': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DP'}),
        }
