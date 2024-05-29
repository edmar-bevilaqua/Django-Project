from django.shortcuts import render
from clientes.models import Cliente
from servicos.models import Services
from .forms import ServiceForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
def update_list(request):
    if request.method == "POST":
        return JsonResponse({'teste':'teste'})