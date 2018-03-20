from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        if request.GET.get('search') is not None:
            ListPatients = patients.objects.filter(nombre__contains=request.GET.get('search').upper()).order_by('nombre')
        else:
            ListPatients = patients.objects.all().order_by('nombre')
        
        for a in ListPatients:
            dt = datetime.datetime.now()
            year_actual = int(dt.strftime("%Y"))

            s = str(a.f_nacimiento)
            ss = s.split('-')
            
            if ss[0] != 'None':
                year_nacimiento = int(ss[0])
                a.f_nacimiento =  year_actual - year_nacimiento

        paginator = Paginator(ListPatients, 9) # Show 25 contacts per page

        page = request.GET.get('page')
        
        try:
            ListPatients = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ListPatients = paginator.page(1)
        except EmptyPage:
            # If page is out osf range (e.g. 9999), deliver last page of results.
            ListPatients = paginator.page(paginator.num_pages)

        return render(request,'patients.html', {'ListPatients':ListPatients,'page_range':paginator.page_range,'count':paginator.num_pages})
        
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
        return redirect('/patient')

@login_required
def patient_Edit (request, id):
    if request.method == 'POST':
        try:
            update = patients.objects.get(id=id)
            update.expediente = request.POST.get('expediente').upper()
            update.nombre = request.POST.get('nombre', '')
            update.a_paterno = request.POST.get('a_paterno', '')
            update.a_materno = request.POST.get('a_materno', '')
            update.telefono = request.POST.get('patelefonossword', '')
            update.celular = request.POST.get('celular', '')
            update.f_nacimiento = datetime.datetime.strptime(request.POST.get('f_nacimiento', ''), "%Y-%m-%d").date()
            update.sexo = request.POST.get('sexo', '')
            update.e_civil = request.POST.get('e_civil', '')
            update.ocupacion = request.POST.get('pocupacionassword', '')
            update.religion = request.POST.get('religion', '')
            update.tipo_sanguinio = request.POST.get('tipo_sanguinio', '')
            update.domicilio = request.POST.get('domicilio', '')
            update.colonia = request.POST.get('colonia', '')
            update.cp = request.POST.get('cp', '')
            update.mail = request.POST.get('mail', '')
            update.estado = request.POST.get('estado', '')
            update.municipio = request.POST.get('municipio', '')
            update.save()   
            messages.success(request, 'Paciente actualizado')
            return redirect ('/patient') 
        except Exception, e:
            messages.error(request, e)
            return redirect ('/patient_edit/'+id) 
        
    try:
        patient = patients.objects.get(id= id)
        s = str(patient.f_nacimiento)
        ss = s.split('-')
        patient.f_nacimiento = ss[0]+'-'+ss[1]+'-'+ss[2]
    except Exception, e:
        messages.error(request,e)
    return render(request,'patients_edit.html', {'patient':patient})
        
@login_required
def patient_Delete(request):
    if request.GET.get('id') is not None and request.user.is_superuser:
        try:
            p = patients.objects.get(id= request.GET.get('id'))
            p.delete()
            messages.success(request,'Paciente eliminado')
        except Exception, e:
            messages.error(request,e)

    return redirect('/patient')