from django.shortcuts import render
from .forms import ServiceForm
from django.http import HttpResponse

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
        return render(request, 'list_services.html')