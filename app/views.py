from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import medics

def index(request): 
    return render(request,'index.html')

def login_user (request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))
        
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Credenciales incorrectas')

    if request.user.is_authenticated:
        return render(request,'manager.html')
    return render(request,'login.html')

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