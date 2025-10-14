# views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Produk, Transaksi, DetailTransaksi
from django.views.decorators.csrf import csrf_exempt
import json

def halaman_kasir(request):
    produk = Produk.objects.all()
    return render(request, 'home.html', {'produk': produk})


@csrf_exempt
def tambah_ke_keranjang(request):
    if request.method == "POST":
        data = json.loads(request.body)
        produk_id = data.get('produk_id')
        jumlah = int(data.get('jumlah'))

        produk = get_object_or_404(Produk, id=produk_id)

        # Buat transaksi baru jika belum ada (dummy)
        transaksi, _ = Transaksi.objects.get_or_create(no_transaksi="120024")

        subtotal = produk.harga_barang * jumlah

        detail = DetailTransaksi.objects.create(
            transaksi=transaksi,
            produk=produk,
            jumlah=jumlah,
            subtotal=subtotal
        )

        return JsonResponse({
            "status": "success",
            "produk": produk.nama_barang,
            "jumlah": jumlah,
            "subtotal": float(subtotal)
        })
