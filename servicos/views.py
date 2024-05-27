from django.shortcuts import render

def new_service(request):
    return render(request, 'new_service.html')
