from django import forms
from .models import NotaKosong, NotaPayment
from kasir.models import Customer

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
