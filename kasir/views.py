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

        # Cek apakah produk sudah ada di keranjang
        existing_detail = DetailTransaksi.objects.filter(transaksi=transaksi, produk=produk).first()
        if existing_detail:
            existing_detail.jumlah += jumlah
            existing_detail.subtotal = existing_detail.jumlah * produk.harga_barang
            existing_detail.save()
            detail = existing_detail
        else:
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
            "jumlah": detail.jumlah,
            "subtotal": float(detail.subtotal),
            "detail_id": detail.id
        })


@csrf_exempt
def update_jumlah(request):
    if request.method == "POST":
        data = json.loads(request.body)
        detail_id = data.get('detail_id')
        action = data.get('action')  # 'tambah' or 'kurangi'

        detail = get_object_or_404(DetailTransaksi, id=detail_id)
        if action == 'tambah':
            detail.jumlah += 1
        elif action == 'kurangi' and detail.jumlah > 1:
            detail.jumlah -= 1
        detail.subtotal = detail.jumlah * detail.produk.harga_barang
        detail.save()

        return JsonResponse({
            "status": "success",
            "jumlah": detail.jumlah,
            "subtotal": float(detail.subtotal)
        })


@csrf_exempt
def hapus_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        detail_id = data.get('detail_id')

        detail = get_object_or_404(DetailTransaksi, id=detail_id)
        detail.delete()

        return JsonResponse({"status": "success"})
