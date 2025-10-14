from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import NotaKosong
from .forms import NotaKosongForm
import json

# Create your views here.
def nota_kosong(request):
    # ambil semua data barang dari database
    daftar_barang = NotaKosong.objects.all()

    if request.method == 'POST':
        form = NotaKosongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barang berhasil ditambahkan!')
            return redirect('nota_kosong')  # arahkan kembali ke halaman yang sama setelah tambah data
    else:
        form = NotaKosongForm()

    konteks = {
        'form': form,
        'daftar_barang': daftar_barang
    }
    return render(request, 'nota_kosong.html', konteks)

@csrf_exempt
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            change = data.get('change', 0)
            item = get_object_or_404(NotaKosong, id=item_id)
            new_quantity = max(0, item.jumlah_barang + change)
            item.jumlah_barang = new_quantity
            item.save()
            return JsonResponse({
                'success': True,
                'new_quantity': new_quantity,
                'new_subtotal': f"{item.subtotal:,.0f}"
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

def edit_item(request, item_id):
    item = get_object_or_404(NotaKosong, id=item_id)
    if request.method == 'POST':
        form = NotaKosongForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barang berhasil diupdate!')
            return redirect('nota_kosong')
    else:
        form = NotaKosongForm(instance=item)
    return render(request, 'nota_kosong.html', {'form': form, 'daftar_barang': NotaKosong.objects.all(), 'edit_item': item})

@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(NotaKosong, id=item_id)
        item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
