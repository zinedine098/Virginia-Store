from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import NotaKosongForm
import json
import uuid

# Create your views here.
def nota_kosong(request):
    if request.method == 'POST':
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
    else:
        form = NotaKosongForm()

    konteks = {
        'form': form,
        'daftar_barang': request.session.get('cart', [])
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
