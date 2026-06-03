from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def login_page(request):
    return render(request, 'login.html')


def mapa_page(request):
    return render(request, 'mapa.html')


def detalle_sala_page(request):
    return render(request, 'detalleSalas.html')


def usuario_page(request):
    return render(request, 'usuario.html')