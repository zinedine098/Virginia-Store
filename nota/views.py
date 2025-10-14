from django.shortcuts import render

# Create your views here.
def nota_kosong(request):
    return render(request, 'nota_kosong.html')