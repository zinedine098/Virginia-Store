from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import NotaKosongForm, NotaPaymentForm, CustomerForm
from .models import NotaPayment, NotaKosong
from kasir.models import Customer
import json
import uuid
from decimal import Decimal

# Create your views here.
def nota_kosong(request):
    # Get or create temporary NotaPayment
    temp_nota_id = request.session.get('temp_nota_id')
    if not temp_nota_id:
        # Create a temporary NotaPayment with dummy data (no customer yet)
        temp_nota = NotaPayment.objects.create(
            customer=None,  # No customer initially
            tanggal_sisa_bayar='2023-01-01',  # Dummy date
            metode_pembayaran='tunai',
            total_bayar=0,
            dp=0,
            sisa=0,
            is_temporary=True
        )
        temp_nota_id = temp_nota.id
        request.session['temp_nota_id'] = temp_nota_id
    else:
        try:
            temp_nota = NotaPayment.objects.get(id=temp_nota_id, is_temporary=True)
        except NotaPayment.DoesNotExist:
            # If temp nota doesn't exist, create new one
            temp_nota = NotaPayment.objects.create(
                customer=None,
                tanggal_sisa_bayar='2023-01-01',
                metode_pembayaran='tunai',
                total_bayar=0,
                dp=0,
                sisa=0,
                is_temporary=True
            )
            temp_nota_id = temp_nota.id
            request.session['temp_nota_id'] = temp_nota_id

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid():
                # Save directly to DB
                gambar_path = None
                if form.cleaned_data['gambar']:
                    from django.core.files.storage import default_storage
                    file_name = default_storage.save(f"gambar_barang/{uuid.uuid4()}_{form.cleaned_data['gambar'].name}", form.cleaned_data['gambar'])
                    gambar_path = file_name
                NotaKosong.objects.create(
                    nota_payment=temp_nota,
                    kode_barang=form.cleaned_data['kode_barang'],
                    nama_barang=form.cleaned_data['nama_barang'],
                    deskripsi=form.cleaned_data['deskripsi'],
                    jumlah_barang=form.cleaned_data['jumlah_barang'],
                    harga=form.cleaned_data['harga'],
                    gambar=gambar_path
                )
                messages.success(request, 'Barang berhasil ditambahkan!')
                return redirect('nota:nota-kosong')
        elif 'submit_payment' in request.POST:
            payment_form = NotaPaymentForm(request.POST)
            if payment_form.is_valid():
                # Get items from DB
                items = NotaKosong.objects.filter(nota_payment=temp_nota)
                if not items.exists():
                    messages.error(request, 'Keranjang kosong!')
                    return redirect('nota:nota-kosong')
                total = sum(item.subtotal for item in items)
                dp = payment_form.cleaned_data['dp']
                sisa = total - dp
                if sisa < 0:
                    messages.error(request, 'DP tidak boleh lebih dari total!')
                    return redirect('nota:nota-kosong')
                # Update temporary NotaPayment with real data
                temp_nota.customer = payment_form.cleaned_data['customer']
                temp_nota.tanggal_sisa_bayar = payment_form.cleaned_data['tanggal_sisa_bayar']
                temp_nota.metode_pembayaran = payment_form.cleaned_data['metode_pembayaran']
                temp_nota.total_bayar = total
                temp_nota.dp = dp
                temp_nota.sisa = sisa
                temp_nota.is_temporary = False
                temp_nota.save()
                # Clear session
                if 'temp_nota_id' in request.session:
                    del request.session['temp_nota_id']
                messages.success(request, 'Nota berhasil disimpan!')
                return redirect('nota:nota-kosong')
    else:
        form = NotaKosongForm()
        payment_form = NotaPaymentForm()

    # Load daftar_barang from DB
    daftar_barang = []
    for item in NotaKosong.objects.filter(nota_payment=temp_nota):
        daftar_barang.append({
            'id': str(item.id),
            'db_id': item.id,
            'kode_barang': item.kode_barang,
            'nama_barang': item.nama_barang,
            'deskripsi': item.deskripsi,
            'jumlah_barang': item.jumlah_barang,
            'harga': float(item.harga),
            'gambar': item.gambar.url if item.gambar else None,
            'subtotal': float(item.subtotal)
        })
    total = sum(item['subtotal'] for item in daftar_barang)

    konteks = {
        'form': form,
        'payment_form': payment_form,
        'daftar_barang': daftar_barang,
        'total': total
    }
    return render(request, 'nota_kosong.html', konteks)

@csrf_exempt
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            change = data.get('change', 0)
            # Update directly in DB
            db_item = NotaKosong.objects.get(id=item_id)
            db_item.jumlah_barang = max(0, db_item.jumlah_barang + change)
            db_item.save()
            return JsonResponse({
                'success': True,
                'new_quantity': db_item.jumlah_barang,
                'new_subtotal': f"{db_item.subtotal:,.0f}"
            })
        except NotaKosong.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'POST':
        try:
            # Delete directly from DB
            NotaKosong.objects.filter(id=item_id).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def cetak_nota_kosong(request):
    notas = NotaPayment.objects.filter(is_temporary=False).order_by('-created_at')
    return render(request, 'cetak_nota_kosong.html', {'notas': notas})

def edit_dp(request, nota_id):
    if request.method == 'POST':
        dp = request.POST.get('dp')
        tanggal_sisa_bayar = request.POST.get('tanggal_sisa_bayar')
        try:
            nota = NotaPayment.objects.get(id=nota_id)
            nota.dp = dp
            nota.tanggal_sisa_bayar = tanggal_sisa_bayar
            nota.sisa = nota.total_bayar - Decimal(dp)
            nota.save()
            return JsonResponse({'success': True})
        except NotaPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Nota not found'})
    return JsonResponse({'success': False})

def edit_nota(request, nota_id):
    try:
        nota = NotaPayment.objects.get(id=nota_id)
    except NotaPayment.DoesNotExist:
        messages.error(request, 'Nota tidak ditemukan.')
        return redirect('nota:cetak-nota-kosong')

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid():
                # Save directly to DB
                gambar_path = None
                if form.cleaned_data['gambar']:
                    from django.core.files.storage import default_storage
                    file_name = default_storage.save(f"gambar_barang/{uuid.uuid4()}_{form.cleaned_data['gambar'].name}", form.cleaned_data['gambar'])
                    gambar_path = file_name
                NotaKosong.objects.create(
                    nota_payment=nota,
                    kode_barang=form.cleaned_data['kode_barang'],
                    nama_barang=form.cleaned_data['nama_barang'],
                    deskripsi=form.cleaned_data['deskripsi'],
                    jumlah_barang=form.cleaned_data['jumlah_barang'],
                    harga=form.cleaned_data['harga'],
                    gambar=gambar_path
                )
                messages.success(request, 'Barang berhasil ditambahkan!')
                return redirect('nota:edit_nota', nota_id=nota_id)
        elif 'update_item' in request.POST:
            item_id = request.POST.get('item_id')
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid() and item_id:
                try:
                    db_item = NotaKosong.objects.get(id=item_id, nota_payment=nota)
                    db_item.kode_barang = form.cleaned_data['kode_barang']
                    db_item.nama_barang = form.cleaned_data['nama_barang']
                    db_item.deskripsi = form.cleaned_data['deskripsi']
                    db_item.jumlah_barang = form.cleaned_data['jumlah_barang']
                    db_item.harga = form.cleaned_data['harga']
                    if form.cleaned_data['gambar']:
                        from django.core.files.storage import default_storage
                        file_name = default_storage.save(f"gambar_barang/{uuid.uuid4()}_{form.cleaned_data['gambar'].name}", form.cleaned_data['gambar'])
                        db_item.gambar = file_name
                    db_item.save()
                    messages.success(request, 'Barang berhasil diupdate!')
                except NotaKosong.DoesNotExist:
                    messages.error(request, 'Item tidak ditemukan.')
                return redirect('nota:edit_nota', nota_id=nota_id)
        elif 'submit_payment' in request.POST:
            payment_form = NotaPaymentForm(request.POST, instance=nota)
            if payment_form.is_valid():
                # Get items from DB
                items = NotaKosong.objects.filter(nota_payment=nota)
                if not items.exists():
                    messages.error(request, 'Keranjang kosong!')
                    return redirect('nota:edit_nota', nota_id=nota_id)

                # Update nota totals
                total = sum(item.subtotal for item in items)
                dp = payment_form.cleaned_data['dp']
                sisa = total - dp
                nota.customer = payment_form.cleaned_data['customer']
                nota.tanggal_sisa_bayar = payment_form.cleaned_data['tanggal_sisa_bayar']
                nota.metode_pembayaran = payment_form.cleaned_data['metode_pembayaran']
                nota.total_bayar = total
                nota.dp = dp
                nota.sisa = sisa
                nota.save()

                messages.success(request, 'Nota berhasil diupdate!')
                return redirect('nota:cetak-nota-kosong')

    form = NotaKosongForm()
    payment_form = NotaPaymentForm(instance=nota)

    # Load daftar_barang from DB
    daftar_barang = []
    for item in NotaKosong.objects.filter(nota_payment=nota):
        daftar_barang.append({
            'id': str(item.id),
            'db_id': item.id,
            'kode_barang': item.kode_barang,
            'nama_barang': item.nama_barang,
            'deskripsi': item.deskripsi,
            'jumlah_barang': item.jumlah_barang,
            'harga': float(item.harga),
            'gambar': item.gambar.url if item.gambar else None,
            'subtotal': float(item.subtotal)
        })
    total = sum(item['subtotal'] for item in daftar_barang)

    konteks = {
        'form': form,
        'payment_form': payment_form,
        'daftar_barang': daftar_barang,
        'total': total,
        'nota': nota
    }
    return render(request, 'edit_nota.html', konteks)

def cetak_pdf(request, nota_id):
    try:
        nota = NotaPayment.objects.get(id=nota_id)
        items = NotaKosong.objects.filter(nota_payment=nota)
        from kasir.models import InformasiToko
        informasi_toko = InformasiToko.objects.first()
        context = {
            'nota': nota,
            'items': items,
            'informasi_toko': informasi_toko,
            'total_bayar': nota.total_bayar,
            'dp': nota.dp,
            'sisa': nota.sisa,
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return HTML as JSON for AJAX requests
            html = render(request, 'nota_struk_modal.html', context).content.decode('utf-8')
            return JsonResponse({'success': True, 'html': html})
        else:
            # Render full page for direct access
            return render(request, 'nota_struk.html', context)
    except NotaPayment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nota not found'})

def nota_palsu(request, nota_id):
    if request.method == 'POST':
        potongan = request.POST.get('potongan')
        try:
            nota = NotaPayment.objects.get(id=nota_id)
            # Apply potongan to each item's harga
            potongan_decimal = Decimal(potongan) / 100
            items = NotaKosong.objects.filter(nota_payment=nota)
            for item in items:
                item.harga = item.harga * (1 - potongan_decimal)
                item.save()
            # Recalculate totals
            nota.total_bayar = sum(item.subtotal for item in items)
            nota.sisa = nota.total_bayar - nota.dp
            nota.save()
            return JsonResponse({'success': True})
        except NotaPayment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Nota not found'})
    return JsonResponse({'success': False})

def cetak_pdf_nota_palsu(request, nota_id):
    try:
        nota = NotaPayment.objects.get(id=nota_id)
        items = NotaKosong.objects.filter(nota_payment=nota)
        persen = request.GET.get('persen', 0)
        persen_decimal = Decimal(persen) / 100 if persen else Decimal(0)
        from kasir.models import InformasiToko
        informasi_toko = InformasiToko.objects.first()
        # Apply potongan to items without modifying originals
        modified_items = []
        for item in items:
            modified_harga = item.harga * (1 - persen_decimal)
            modified_subtotal = modified_harga * item.jumlah_barang
            modified_items.append({
                'id': item.id,
                'kode_barang': item.kode_barang,
                'nama_barang': item.nama_barang,
                'deskripsi': item.deskripsi,
                'jumlah_barang': item.jumlah_barang,
                'harga': modified_harga,
                'gambar': item.gambar,
                'subtotal': modified_subtotal
            })
        # Recalculate totals
        total_bayar = sum(item['subtotal'] for item in modified_items)
        dp = nota.dp
        sisa = total_bayar - dp
        context = {
            'nota': nota,
            'items': modified_items,
            'informasi_toko': informasi_toko,
            'total_bayar': total_bayar,
            'dp': dp,
            'sisa': sisa,
        }
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return HTML as JSON for AJAX requests
            html = render(request, 'nota_struk_modal.html', context).content.decode('utf-8')
            return JsonResponse({'success': True, 'html': html})
        else:
            # Render full page for direct access
            return render(request, 'nota_struk_modal.html', context)
    except NotaPayment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nota not found'})

@csrf_exempt
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return JsonResponse({
                'success': True,
                'customer_id': customer.id,
                'customer_name': customer.nama
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False})
