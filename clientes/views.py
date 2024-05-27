from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pet
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import re

def clientes(request):
    clientes_list = Cliente.objects.all()
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
        elif Cliente.objects.filter(email=email).exists():
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'cpf':cpf, 'pets' : zip(pets, datas_nascimentos, portes)})
        else:
            cliente = Cliente(
                nome = nome,
                sobrenome = sobrenome,
                email = email,
                cpf = cpf
            )
            cliente.save()
            print(cliente)
            
            for pet, data, porte in zip(pets, datas_nascimentos, portes):
                pet = Pet(
                    nome_pet = pet,
                    data_nascimento_pet = data,
                    porte = porte,
                    cliente = cliente
                )
                pet.save()
    return render(request, 'clientes.html', {'clientes' : clientes_list})

def atualizar_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    query_cliente = Cliente.objects.filter(id=id_cliente)
    query_pets = Pet.objects.filter(cliente=query_cliente[0])

    json_cliente = json.loads(serializers.serialize('json', query_cliente))[0]['fields']
    json_pets = json.loads(serializers.serialize('json', query_pets))
    json_pets = [{'fields': pet['fields'], 'id': pet['pk']} for pet in json_pets]
    
    json_response = {'clientes': json_cliente, 'pets': json_pets}

    return JsonResponse(json_response)

@csrf_exempt
def add_pet(request, id):
    cliente = Cliente.objects.filter(id = id)[0]
    pet = Pet(
        nome_pet = request.POST.get('pet'),
        data_nascimento_pet = request.POST.get('data-nascimento'),
        porte = request.POST.get('porte'),
        cliente = cliente   
    )
    pet.save()
    return redirect('../')

@csrf_exempt
def atualiza_pet(request, id):
    pet = Pet.objects.get(id=id)

    nome_pet = request.POST.get('pet')
    data_nascimento = request.POST.get('data-nascimento')
    porte = request.POST.get('porte')

    if (pet.nome_pet != nome_pet) or (str(pet.data_nascimento_pet) != data_nascimento) or (pet.porte != porte):
        pet.nome_pet = nome_pet
        pet.data_nascimento_pet = data_nascimento
        pet.porte = porte
        pet.save()
        return HttpResponse("Dados alterados")
    else:
        return HttpResponse("Os dados não foram modificados")

def deleta_pet(request, id):
    pet = Pet.objects.get(id=id)
    
    pet.delete()
    return HttpResponse('Pet deletado :(')