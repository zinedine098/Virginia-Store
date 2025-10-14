from django import forms
from .models import NotaKosong

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
