from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pet
import re

def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes' : clientes_list})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        pets = request.POST.getlist('pet')
        datas_nascimentos = request.POST.getlist('data-nascimento')
        portes = request.POST.getlist('porte')
        
        cliente = Cliente.objects.filter(cpf=cpf)
        if cliente.exists():
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'email':email, 'pets' : zip(pets, datas_nascimentos, portes)})
        elif not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'cpf':cpf, 'pets' : zip(pets, datas_nascimentos, portes)})
        else:
            cliente = Cliente(
                nome = nome,
                sobrenome = sobrenome,
                email = email,
                cpf = cpf
            )
            cliente.save()
            
            for pet, data, porte in zip(pets, datas_nascimentos, portes):
                pet = Pet(
                    nome_pet = pet,
                    data_nascimento_pet = data,
                    porte = porte,
                    cliente = cliente
                )
                pet.save()
        
        
    print(request.POST)
    return HttpResponse("teste")

def atualizar_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    Cliente.objects.filter(id=id_cliente)
    return JsonResponse({"teste": 1})
        
