import json
from django.shortcuts import render, get_object_or_404
from clientes.models import Cliente
from servicos.models import Services
from .forms import ServiceForm
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.urls import reverse
from fpdf import FPDF
from io import BytesIO

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

# This method lists all services.
def list_services(request):
    if request.method == "GET":
        services = Services.objects.all()
        clients = Cliente.objects.all()
        if len(services) > 0:
            return render(request, 'list_services.html', {'services':services, 'clients':clients})
        else:
            return HttpResponse("There is no service to be listed!")

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
    

def generate_SO(request, identifier):
    service = get_object_or_404(Services, identifier = identifier)
    
    pdf = FPDF()
    pdf.add_page()

    

    pdf.rect(5., 5., 200., 287.)

    pdf.image("templates\static\servicos\images\logo.jpg", 79, 10, 52, 40)

    pdf.set_xy(10., 53)
    pdf.set_font(family='Arial', style='B', size=32)
    pdf.cell(w=0, h=10, border=0, txt="J&J PETSHOP", align='C', ln=1)
    pdf.cell(w=0, h=10, border=0, txt="", align='L', ln=1)
    pdf.set_title("J&J PETSHOP")

    pdf.set_font(family='Arial', style='B', size=16)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(w=35, h=10, border=0, txt="Client:", align='L', ln=0)
    pdf.cell(w=0, h=10, border=1, txt=f"{service.client.nome} {service.client.sobrenome}", align='L', ln=1)
    pdf.cell(w=35, h=10, border=0, txt="CPF:", align='L', ln=0)
    pdf.cell(w=0, h=10, border=1, txt=f"{service.client.cpf}", align='L', ln=1)
    pdf.cell(w=35, h=10, border=0, txt="Protocol:", align='L', ln=0)
    pdf.cell(w=0, h=10, border=1, txt=f"{service.protocol}", align='L', ln=1)

    pdf.cell(w=35, h=10, border=0, txt="", align='L', ln=1)

    pdf.cell(w=35, h=10, border=0, txt="Initial Date:", align='L', ln=0)
    pdf.cell(w=0, h=10, border=1, txt=f"{service.date_init}", align='L', ln=1)
    pdf.cell(w=35, h=10, border=0, txt="Final Date:", align='L', ln=0)
    pdf.cell(w=0, h=10, border=1, txt=f"{service.date_final}", align='L', ln=1)

    pdf.cell(w=35, h=10, border=0, txt="", align='L', ln=1)

    pdf.cell(w=35, h=10, border=0, txt="Service Categories:", align='L', ln=2)

    for category in service.service_category.all():
        pdf.cell(w=160, h=10, border=1, txt=f"-   {category.get_title_display()}", align='L', ln=0)
        pdf.cell(w=30, h=10, border=1, txt=f"R$ {category.price}", align='C', ln=1)
    pdf.cell(w=160, h=10, border=0, txt="Total     ", align='R', ln=0)
    pdf.cell(w=30, h=10, border=0, txt=f"R$ {service.total_price()}", align='C', ln=1)
    
    pdf.image("templates\static\servicos\images\dog.jpg", 60, 200, 90, 90)

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)

    return FileResponse(pdf_bytes, as_attachment=True, filename=f"SO-{service.protocol}.pdf")