from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import NotaKosongForm, NotaPaymentForm
from .models import NotaPayment, NotaKosong
import json
import uuid
from decimal import Decimal

# Create your views here.
def nota_kosong(request):
    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid():
                # Instead of saving to DB, add to session cart
                cart = request.session.get('cart', [])
                gambar_url = None
                if form.cleaned_data['gambar']:
                    # Save the file temporarily and get URL
                    from django.core.files.storage import default_storage
                    file_name = default_storage.save(f"temp_{uuid.uuid4()}_{form.cleaned_data['gambar'].name}", form.cleaned_data['gambar'])
                    gambar_url = default_storage.url(file_name)
                item = {
                    'id': str(uuid.uuid4()),
                    'kode_barang': form.cleaned_data['kode_barang'],
                    'nama_barang': form.cleaned_data['nama_barang'],
                    'deskripsi': form.cleaned_data['deskripsi'],
                    'jumlah_barang': form.cleaned_data['jumlah_barang'],
                    'harga': float(form.cleaned_data['harga']),
                    'gambar': gambar_url,
                    'subtotal': float(form.cleaned_data['harga']) * form.cleaned_data['jumlah_barang']
                }
                cart.append(item)
                request.session['cart'] = cart
                messages.success(request, 'Barang berhasil ditambahkan ke keranjang!')
                return redirect('nota:nota-kosong')
        elif 'submit_payment' in request.POST:
            payment_form = NotaPaymentForm(request.POST)
            if payment_form.is_valid():
                cart = request.session.get('cart', [])
                if not cart:
                    messages.error(request, 'Keranjang kosong!')
                    return redirect('nota:nota-kosong')
                total = sum(item['subtotal'] for item in cart)
                dp = float(payment_form.cleaned_data['dp'])
                sisa = total - dp
                if sisa < 0:
                    messages.error(request, 'DP tidak boleh lebih dari total!')
                    return redirect('nota:nota-kosong')
                # Save to database
                nota_payment = NotaPayment.objects.create(
                    customer=payment_form.cleaned_data['customer'],
                    tanggal_sisa_bayar=payment_form.cleaned_data['tanggal_sisa_bayar'],
                    metode_pembayaran=payment_form.cleaned_data['metode_pembayaran'],
                    total_bayar=total,
                    dp=dp,
                    sisa=sisa
                )
                for item in cart:
                    NotaKosong.objects.create(
                        nota_payment=nota_payment,
                        kode_barang=item['kode_barang'],
                        nama_barang=item['nama_barang'],
                        deskripsi=item['deskripsi'],
                        jumlah_barang=item['jumlah_barang'],
                        harga=item['harga'],
                        gambar=item['gambar']
                    )
                # Clear cart
                request.session['cart'] = []
                messages.success(request, 'Nota berhasil disimpan!')
                return redirect('nota:nota-kosong')
    else:
        form = NotaKosongForm()
        payment_form = NotaPaymentForm()

    cart = request.session.get('cart', [])
    total = sum(item['subtotal'] for item in cart)

    konteks = {
        'form': form,
        'payment_form': payment_form,
        'daftar_barang': cart,
        'total': total
    }
    return render(request, 'nota_kosong.html', konteks)

@csrf_exempt
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            change = data.get('change', 0)
            cart = request.session.get('cart', [])
            for item in cart:
                if item['id'] == item_id:
                    item['jumlah_barang'] = max(0, item['jumlah_barang'] + change)
                    item['subtotal'] = item['harga'] * item['jumlah_barang']
                    break
            request.session['cart'] = cart
            item = next((i for i in cart if i['id'] == item_id), None)
            if item:
                return JsonResponse({
                    'success': True,
                    'new_quantity': item['jumlah_barang'],
                    'new_subtotal': f"{item['subtotal']:,.0f}"
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['id'] != item_id]
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def cetak_nota_kosong(request):
    notas = NotaPayment.objects.all().order_by('-created_at')
    return render(request, 'cetak_nota_kosong.html', {'notas': notas})

def edit_dp(request, nota_id):
    if request.method == 'POST':
        dp = request.POST.get('dp')
        try:
            nota = NotaPayment.objects.get(id=nota_id)
            nota.dp = dp
            nota.sisa = nota.total_bayar - Decimal(dp)
            nota.save()
            return JsonResponse({'success': True})
        except NotaPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Nota not found'})
    return JsonResponse({'success': False})

def edit_nota(request, nota_id):
    # Implement edit nota functionality
    return JsonResponse({'success': True, 'message': 'Edit nota functionality'})

def cetak_pdf(request, nota_id):
    # Implement cetak PDF functionality
    return JsonResponse({'success': True, 'message': 'Cetak PDF functionality'})

def nota_palsu(request, nota_id):
    if request.method == 'POST':
        potongan = request.POST.get('potongan')
        try:
            nota = NotaPayment.objects.get(id=nota_id)
            # Apply potongan to total_bayar or sisa
            # For example, reduce sisa by potongan percent
            potongan_decimal = Decimal(potongan) / 100
            nota.sisa = nota.sisa * (1 - potongan_decimal)
            nota.save()
            return JsonResponse({'success': True})
        except NotaPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Nota not found'})
    return JsonResponse({'success': False})
