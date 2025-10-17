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
                    # If this is a database item, update the DB
                    if 'db_id' in item:
                        from .models import NotaKosong
                        db_item = NotaKosong.objects.get(id=item['db_id'])
                        db_item.jumlah_barang = item['jumlah_barang']
                        db_item.save()
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
        # Find the item to delete
        item_to_delete = None
        for item in cart:
            if item['id'] == item_id:
                item_to_delete = item
                break

        if item_to_delete and 'db_id' in item_to_delete:
            # Delete from database
            from .models import NotaKosong
            NotaKosong.objects.filter(id=item_to_delete['db_id']).delete()

        # Remove from cart
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

    # Initialize cart from session, or load from DB if session is empty
    cart = request.session.get('cart', [])
    if not cart:
        # Load existing items into cart only if session cart is empty
        cart = []
        for item in nota.items.all():
            cart.append({
                'id': str(uuid.uuid4()),
                'db_id': item.id,
                'kode_barang': item.kode_barang,
                'nama_barang': item.nama_barang,
                'deskripsi': item.deskripsi,
                'jumlah_barang': item.jumlah_barang,
                'harga': float(item.harga),
                'gambar': item.gambar.url if item.gambar else None,
                'subtotal': float(item.subtotal)
            })
        request.session['cart'] = cart

    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid():
                gambar_url = None
                if form.cleaned_data['gambar']:
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
                return redirect('nota:edit_nota', nota_id=nota_id)
        elif 'update_item' in request.POST:
            item_id = request.POST.get('item_id')
            form = NotaKosongForm(request.POST, request.FILES)
            if form.is_valid() and item_id:
                for item in cart:
                    if item['id'] == item_id:
                        item['kode_barang'] = form.cleaned_data['kode_barang']
                        item['nama_barang'] = form.cleaned_data['nama_barang']
                        item['deskripsi'] = form.cleaned_data['deskripsi']
                        item['jumlah_barang'] = form.cleaned_data['jumlah_barang']
                        item['harga'] = float(form.cleaned_data['harga'])
                        if form.cleaned_data['gambar']:
                            from django.core.files.storage import default_storage
                            file_name = default_storage.save(f"temp_{uuid.uuid4()}_{form.cleaned_data['gambar'].name}", form.cleaned_data['gambar'])
                            item['gambar'] = default_storage.url(file_name)
                        item['subtotal'] = item['harga'] * item['jumlah_barang']
                        break
                request.session['cart'] = cart
                messages.success(request, 'Barang berhasil diupdate!')
                return redirect('nota:edit_nota', nota_id=nota_id)
        elif 'submit_payment' in request.POST:
            payment_form = NotaPaymentForm(request.POST, instance=nota)
            if payment_form.is_valid():
                if not cart:
                    messages.error(request, 'Keranjang kosong!')
                    return redirect('nota:edit_nota', nota_id=nota_id)

                # Get existing items
                existing_items = {item.id: item for item in nota.items.all()}

                # Track items in cart
                cart_item_ids = set()
                for item in cart:
                    db_id = item.get('db_id')
                    if db_id and db_id in existing_items:
                        # Update existing
                        existing_item = existing_items[db_id]
                        existing_item.kode_barang = item['kode_barang']
                        existing_item.nama_barang = item['nama_barang']
                        existing_item.deskripsi = item['deskripsi']
                        existing_item.jumlah_barang = item['jumlah_barang']
                        existing_item.harga = item['harga']
                        existing_item.gambar = item['gambar']
                        existing_item.save()
                        cart_item_ids.add(db_id)
                    else:
                        # Create new
                        NotaKosong.objects.create(
                            nota_payment=nota,
                            kode_barang=item['kode_barang'],
                            nama_barang=item['nama_barang'],
                            deskripsi=item['deskripsi'],
                            jumlah_barang=item['jumlah_barang'],
                            harga=item['harga'],
                            gambar=item['gambar']
                        )

                # Delete items not in cart
                for db_id, item in existing_items.items():
                    if db_id not in cart_item_ids:
                        item.delete()

                # Update nota totals
                total = sum(item['subtotal'] for item in cart)
                dp = float(payment_form.cleaned_data['dp'])
                sisa = total - dp
                nota.customer = payment_form.cleaned_data['customer']
                nota.tanggal_sisa_bayar = payment_form.cleaned_data['tanggal_sisa_bayar']
                nota.metode_pembayaran = payment_form.cleaned_data['metode_pembayaran']
                nota.total_bayar = total
                nota.dp = dp
                nota.sisa = sisa
                nota.save()

                # Clear cart
                request.session['cart'] = []
                messages.success(request, 'Nota berhasil diupdate!')
                return redirect('nota:cetak-nota-kosong')

    form = NotaKosongForm()
    payment_form = NotaPaymentForm(instance=nota)
    total = sum(item['subtotal'] for item in cart)

    konteks = {
        'form': form,
        'payment_form': payment_form,
        'daftar_barang': cart,
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
            # Apply potongan to total_bayar or sisa
            # For example, reduce sisa by potongan percent
            potongan_decimal = Decimal(potongan) / 100
            nota.sisa = nota.sisa * (1 - potongan_decimal)
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
        # Apply potongan to items
        modified_items = []
        for item in items:
            modified_item = item
            modified_item.harga = item.harga * (1 - persen_decimal)
            modified_items.append(modified_item)
        # Recalculate totals
        total_bayar = sum(item.subtotal for item in modified_items)
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
