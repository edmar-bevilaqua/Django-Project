import json
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from servicos.models import Services
from .forms import ServiceForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse

# Defining the method to handle GET requests and render the /services.html/ page
def new_service(request):
    if request.method == "GET":
        form = ServiceForm()
        return render(request, 'new_service.html', {'form': form})
    elif request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            form = ServiceForm()
            print("Arquivo salvo com sucesso")
            return render(request, 'new_service.html', {'form': form})
        else:
            print("Houve um problema salvando o arquivo")
            return render(request, 'new_service.html', {'form': form})

def list_services(request):
    if request.method == "GET":
        services = Services.objects.all()
        clients = Cliente.objects.all()
        print(type(services[0]))
        return render(request, 'list_services.html', {'services':services, 'clients':clients})

# This method updates the services list based on the client selected
@csrf_exempt
def update_list(request):
    if request.method == "POST":
        client_id = request.POST.get('client_id')
        client = Cliente.objects.filter(id=client_id)
        service = Services.objects.filter(client = client[0])
        
        if service.exists():
            print(service[0].total_price())
            service_json = json.loads(serializers.serialize('json', service))
            service_fields = [serv['fields'] for serv in service_json]
            service_pks = [serv['pk'] for serv in service_json]
            total_price = [serv.total_price() for serv in service]
            data = {
                'service_fields': service_fields,
                'service_pks': service_pks,
                'client_name': client[0].nome,
                'total_price': total_price
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'teste':'Cliente não existe'})

# This method returns a view of a specific service
def view_service(request, identifier):
    if request.method == "GET":
        service = get_object_or_404(Services, identifier=identifier)
        return render(request, 'service.html', {'service_details': service})