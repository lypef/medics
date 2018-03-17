from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import medics

def index(request): 
    return render(request,'index.html')

def user_login (request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
        
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Credenciales incorrectas')

    if request.user.is_authenticated:
        return render(request,'manager.html')
    return render(request,'login.html')

def user_logout (request):
    if request.user.is_authenticated:
        messages.info(request, 'Hasta pronto: ' + request.user.first_name + ' '  + request.user.last_name)
        logout(request)            
        return redirect('/manager')
    return redirect('/manager')

def Medic_Add (request):
    if request.method == 'POST':
        insert = medics(
                username = request.POST.get('username', '').upper(), 
    			password = request.POST.get('password', ''),
    			name = '10',
    			telefono = '10',
    			movil = '10',
    			email = '10@h.com'
    			)
    	insert.save()
        return redirect('/medic_add/')
    return render(request,'Medic_add.html')