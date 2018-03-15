from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from models import medics


def index(request): 
    return render(request,'index.html')

def login_user (request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(username='root', password='root')
        
        if user is not None:
            print("si")
        else:
            print("NO")
            
    if request.user.is_authenticated():
        return render(request,'a.html')
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