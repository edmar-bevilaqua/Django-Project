from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Pet
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
import re

# This view is for the main page (/clientes/), it can operade either GET or POST
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

# This is the view to list the informations about the client selected by the user
def atualizar_cliente(request):
    id_cliente = request.POST.get('id_cliente')

    query_cliente = Cliente.objects.filter(id=id_cliente)
    query_pets = Pet.objects.filter(cliente=query_cliente[0])

    json_cliente = json.loads(serializers.serialize('json', query_cliente))[0]['fields']
    json_pets = json.loads(serializers.serialize('json', query_pets))
    json_pets = [{'fields': pet['fields'], 'id': pet['pk']} for pet in json_pets]
    
    json_response = {'clientes': json_cliente, 'pets': json_pets, 'cliente_id':int(id_cliente)}

    return JsonResponse(json_response)

# This method is used to add a new pet to the client selected by the user
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
    return redirect(reverse(clientes))

# This method updates the information about a selected pet
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

# This method deletes a pet
def deleta_pet(request, id):
    try:
        pet = Pet.objects.get(id=id)
        
        pet.delete()
        return redirect(reverse('clientes')+f'?aba=atualizar_cliente&id_cliente={id}')
    except:
        return redirect(reverse('clientes')+f'?aba=atualizar_cliente&id_cliente={id}')

# This method updates a client information
def atualiza_cliente(request, id):
    body = json.loads(request.body)
        
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']
    
    cliente = get_object_or_404(Cliente, id=id)
    
    cliente.nome = nome
    cliente.sobrenome = sobrenome
    cliente.email = email
    cliente.cpf = cpf
    
    try:
        cliente.save()
        return JsonResponse({'status':'200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})
    except:
        print('Atualização no banco falhou!')
        return JsonResponse({'status':'500', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf': cpf})

def list_clients(request):
    if request.method == 'GET':
        client_list = Cliente.objects.all()
        pets_dict_ids = {}
        for num in [pet.cliente.id for pet in Pet.objects.all()]:
            if num in pets_dict_ids:
                pets_dict_ids[num] += 1
            else:
                pets_dict_ids[num] = 1
        return render(request, 'list_clients.html', {'clients' : client_list, 'pets_dict_ids': pets_dict_ids})