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

        if produk.stok < jumlah:
            return JsonResponse({
                "status": "error",
                "message": "Stok tidak cukup!"
            })

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

        # Kurangi stok
        produk.stok -= jumlah
        produk.save()

        return JsonResponse({
            "status": "success",
            "produk": produk.nama_barang,
            "jumlah": detail.jumlah,
            "subtotal": float(detail.subtotal),
            "detail_id": detail.id,
            "new_stok": produk.stok
        })


@csrf_exempt
def update_jumlah(request):
    if request.method == "POST":
        data = json.loads(request.body)
        detail_id = data.get('detail_id')
        action = data.get('action')  # 'tambah' or 'kurangi'

        detail = get_object_or_404(DetailTransaksi, id=detail_id)
        produk = detail.produk
        if action == 'tambah':
            if produk.stok > 0:
                detail.jumlah += 1
                produk.stok -= 1
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Stok tidak cukup!"
                })
        elif action == 'kurangi' and detail.jumlah > 1:
            detail.jumlah -= 1
            produk.stok += 1
        detail.subtotal = detail.jumlah * produk.harga_barang
        detail.save()
        produk.save()

        return JsonResponse({
            "status": "success",
            "jumlah": detail.jumlah,
            "subtotal": float(detail.subtotal),
            "produk_id": produk.id,
            "new_stok": produk.stok
        })


@csrf_exempt
def hapus_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        detail_id = data.get('detail_id')

        detail = get_object_or_404(DetailTransaksi, id=detail_id)
        produk = detail.produk
        # Kembalikan stok
        produk.stok += detail.jumlah
        produk.save()
        detail.delete()

        return JsonResponse({
            "status": "success",
            "produk_id": produk.id,
            "new_stok": produk.stok
        })
