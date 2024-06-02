from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == "GET":
        return render(request, 'authenticate/login.html', {})
    elif request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index.html')
        else:
            messages.success(request, ("There were a mistake, try again!"))
            return redirect('login_user')
        
def logout_user(request):
    if request.method == "GET":
        logout(request)
        messages.success(request, ("You have succesfully logged out!"))
        return redirect('index.html')