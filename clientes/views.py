from django.shortcuts import render
from django.http import HttpResponse


def clientes(request):
    if request.method == "GET":
        return render(request, 'clientes.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        pets = request.POST.getlist('pet')
        datas_nascimentos = request.POST.getlist('data-nascimento')
        portes = request.POST.getlist('porte')
        
    print(request.POST)
    return HttpResponse("teste")
        
