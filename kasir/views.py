# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Produk, Transaksi, DetailTransaksi, Customer, InformasiToko
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Max
from decimal import Decimal
import json

def halaman_kasir(request):
    produk = Produk.objects.all()
    # Get or create current transaksi in session
    transaksi_id = request.session.get('current_transaksi_id')
    if not transaksi_id:
        # Generate new no_transaksi
        max_no = Transaksi.objects.aggregate(Max('no_transaksi'))['no_transaksi__max']
        if max_no:
            new_no = str(int(max_no) + 1).zfill(6)
        else:
            new_no = "000001"
        transaksi = Transaksi.objects.create(no_transaksi=new_no)
        request.session['current_transaksi_id'] = transaksi.id
    return render(request, 'home.html', {'produk': produk})


def get_keranjang(request):
    transaksi_id = request.session.get('current_transaksi_id')
    if not transaksi_id:
        return JsonResponse({"details": []})
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    details = DetailTransaksi.objects.filter(transaksi=transaksi)
    details_data = []
    for detail in details:
        details_data.append({
            "detail_id": detail.id,
            "produk": detail.produk.nama_barang,
            "harga": float(detail.produk.harga_barang),
            "jumlah": detail.jumlah,
            "subtotal": float(detail.subtotal),
            "produk_id": detail.produk.id
        })
    return JsonResponse({"details": details_data})


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

        # Get current transaksi from session
        transaksi_id = request.session.get('current_transaksi_id')
        if not transaksi_id:
            return JsonResponse({"status": "error", "message": "No active transaction"})
        transaksi = get_object_or_404(Transaksi, id=transaksi_id)

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


def halaman_bayar(request):
    transaksi_id = request.session.get('current_transaksi_id')
    if not transaksi_id:
        return redirect('halaman_kasir')
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    details = DetailTransaksi.objects.filter(transaksi=transaksi)
    total = details.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    customers = Customer.objects.all()
    return render(request, 'bayar.html', {
        'transaksi': transaksi,
        'details': details,
        'total': total,
        'customers': customers
    })


def proses_bayar(request):
    if request.method == 'POST':
        transaksi_id = request.session.get('current_transaksi_id')
        if not transaksi_id:
            return redirect('halaman_kasir')
        transaksi = get_object_or_404(Transaksi, id=transaksi_id)
        details = DetailTransaksi.objects.filter(transaksi=transaksi)
        total = details.aggregate(Sum('subtotal'))['subtotal__sum'] or 0

        customer_id = request.POST.get('customer')
        payment_method = request.POST.get('payment_method')
        try:
            amount_paid = float(request.POST.get('amount_paid', 0))
        except ValueError:
            messages.error(request, "Jumlah dibayar tidak valid.")
            return redirect('halaman_bayar')

        if amount_paid < float(total):
            messages.error(request, "Jumlah dibayar kurang dari total.")
            return redirect('halaman_bayar')

        change = amount_paid - float(total)

        if customer_id:
            try:
                customer = get_object_or_404(Customer, id=customer_id)
                transaksi.customer = customer
            except:
                pass
        transaksi.payment_method = payment_method
        transaksi.amount_paid = amount_paid
        transaksi.change = change
        transaksi.save()

        # Clear session to reset cart
        del request.session['current_transaksi_id']
        messages.success(request, "Transaksi berhasil!")

        # Fetch informasi_toko for receipt
        informasi_toko = InformasiToko.objects.first()

        # Render bayar.html with receipt data and show_modal flag
        return render(request, 'bayar.html', {
            'transaksi': transaksi,
            'details': details,
            'total': total,
            'customers': Customer.objects.all(),  # Keep customers for form
            'informasi_toko': informasi_toko,
            'show_modal': True
        })
    return redirect('halaman_kasir')


def halaman_struk(request, transaksi_id):
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    details = DetailTransaksi.objects.filter(transaksi=transaksi)
    total = details.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    informasi_toko = InformasiToko.objects.first()
    return render(request, 'struk.html', {
        'transaksi': transaksi,
        'details': details,
        'total': total,
        'informasi_toko': informasi_toko
    })


def get_produk_by_barcode(request):
    barcode = request.GET.get('barcode')
    if not barcode:
        return JsonResponse({"status": "error", "message": "Barcode tidak diberikan"})
    try:
        produk = Produk.objects.get(barcode=barcode)
        data = {
            "status": "success",
            "id": produk.id,
            "nama_barang": produk.nama_barang,
            "harga_barang": float(produk.harga_barang),
            "stok": produk.stok,
            "gambar": produk.gambar.url if produk.gambar else ""
        }
        return JsonResponse(data)
    except Produk.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Produk tidak ditemukan"})


def batalkan_transaksi(request):
    transaksi_id = request.session.get('current_transaksi_id')
    if not transaksi_id:
        return redirect('halaman_kasir')
    transaksi = get_object_or_404(Transaksi, id=transaksi_id)
    details = DetailTransaksi.objects.filter(transaksi=transaksi)
    for detail in details:
        produk = detail.produk
        produk.stok += detail.jumlah
        produk.save()
    details.delete()
    transaksi.delete()
    # Clear session
    del request.session['current_transaksi_id']
    return redirect('halaman_kasir')
