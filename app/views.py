from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from models import patients

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
        if request.GET.get('next', '/') == '/':
            return render(request,'manager.html')
        else:
            return redirect(request.GET.get('next', '/'))
    return render(request,'login.html')

def user_logout (request):
    if request.user.is_authenticated:
        messages.info(request, 'Hasta pronto: ' + request.user.first_name + ' '  + request.user.last_name)
        logout(request)            
        return redirect('/manager')
    return redirect('/manager')

@login_required
def patient (request):
    if request.method == 'GET':
        ListPatients = patients.objects.all().order_by('nombre')
        for a in ListPatients:
            dt = datetime.datetime.now()
            year_actual = int(dt.strftime("%Y"))

            s = str(a.f_nacimiento)
            ss = s.split('-')
            
            if ss[0] != 'None':
                year_nacimiento = int(ss[0])
                a.f_nacimiento =  year_actual - year_nacimiento

            
        return render(request,'patients.html', {'ListPatients':ListPatients})
    		
    if request.method == 'POST':
        insert = patients(
                expediente = request.POST.get('expediente', '').upper(), 
    			nombre = request.POST.get('nombre', ''),
                a_paterno = request.POST.get('a_paterno', ''),
                a_materno = request.POST.get('a_materno', ''),
                telefono = request.POST.get('patelefonossword', ''),
                celular = request.POST.get('celular', ''),
                f_nacimiento = datetime.datetime.strptime(request.POST.get('f_nacimiento', ''), "%Y-%m-%d").date(),
                sexo = request.POST.get('sexo', ''),
                e_civil = request.POST.get('e_civil', ''),
                ocupacion = request.POST.get('pocupacionassword', ''),
                religion = request.POST.get('religion', ''),
                tipo_sanguinio = request.POST.get('tipo_sanguinio', ''),
                domicilio = request.POST.get('domicilio', ''),
                colonia = request.POST.get('colonia', ''),
                cp = request.POST.get('cp', ''),
                mail = request.POST.get('mail', ''),
                estado = request.POST.get('estado', ''),
                municipio = request.POST.get('municipio', '')
    			)
    	insert.save()
        messages.success(request,'Paciente agregado')
        return render(request,'patients.html')
    