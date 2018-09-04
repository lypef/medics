from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer
from io import BytesIO
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from django.contrib.auth.models import User
from models import patients, Procedure, receta, receta_procedures, diary, properties
from django.core.files.storage import FileSystemStorage
from decimal import Decimal
from django.core.mail import EmailMessage

def index(request):
    #return render(request,'index.html')
    return redirect("/manager")

def user_login (request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password', ''))

        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'Credenciales incorrectas')

    if request.user.is_authenticated:
        if request.GET.get('next', '/') == '/':
            for tmp in properties.objects.all():
                propiedades = tmp
            return render(request,'manager.html', {'propiedades':propiedades})
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

            ListPatients = patients.objects.exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).filter(id__contains=request.GET.get('search').upper()).order_by('nombre')

            if len(ListPatients) < 1:
                ListPatients = patients.objects.exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).filter(nombre__contains=request.GET.get('search').upper()).order_by('nombre')
            if len(ListPatients) < 1:
                ListPatients = patients.objects.exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).filter(a_paterno__contains=request.GET.get('search').upper()).order_by('nombre')
            if len(ListPatients) < 1:
                ListPatients = patients.objects.exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).filter(a_materno__contains=request.GET.get('search').upper()).order_by('nombre')
            if len(ListPatients) < 1:
                ListPatients = patients.objects.exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).filter(id_monedero__contains=int(request.GET.get('search'))).order_by('nombre')
        else:
            ListPatients = patients.objects.all().exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).order_by('nombre')

        agenda = diary.objects.all().order_by('-id')

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
        for tmp in properties.objects.all():
            propiedades = tmp
        return render(request,'patients.html', {'ListPatients':ListPatients,'page_range':paginator.page_range,'count':paginator.num_pages, 'agenda':agenda, 'propiedades':propiedades})

    if request.method == 'POST':
        insert = patients(
                expediente = request.POST.get('expediente', '').upper(),
    			nombre = request.POST.get('nombre', '').upper(),
                a_paterno = request.POST.get('a_paterno', '').upper(),
                a_materno = request.POST.get('a_materno', '').upper(),
                telefono = request.POST.get('telefono', ''),
                celular = request.POST.get('celular', ''),
                f_nacimiento = datetime.datetime.strptime(request.POST.get('f_nacimiento', ''), "%Y-%m-%d").date(),
                sexo = request.POST.get('sexo', ''),
                e_civil = request.POST.get('e_civil', ''),
                ocupacion = request.POST.get('ocupacion', ''),
                religion = request.POST.get('religion', ''),
                tipo_sanguinio = request.POST.get('tipo_sanguinio', ''),
                domicilio = request.POST.get('domicilio', ''),
                colonia = request.POST.get('colonia', ''),
                cp = request.POST.get('cp', ''),
                id_monedero = request.POST.get('id_monedero', ''),
                monedero = 0,
                mail = request.POST.get('mail', ''),
                estado = request.POST.get('estado', ''),
                municipio = request.POST.get('municipio', ''),
                nopatologicos = request.POST.get('nopatologicos', '').upper(),
                patologicos = request.POST.get('patologicos', '').upper(),
                ginecologos = request.POST.get('ginecologos', '').upper(),
                andrologicos = request.POST.get('andrologicos', '').upper(),
                perinatales = request.POST.get('perinatales', '').upper(),
                quirurgicos = request.POST.get('quirurgicos', '').upper(),
                alergias = request.POST.get('alergias', '').upper(),
                observaciones = request.POST.get('observaciones', '').upper(),
                medic = User.objects.get(id=request.user.id)
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
            update.nombre = request.POST.get('nombre', '').upper()
            update.a_paterno = request.POST.get('a_paterno', '').upper()
            update.a_materno = request.POST.get('a_materno', '').upper()
            update.telefono = request.POST.get('telefono', '')
            update.celular = request.POST.get('celular', '')
            update.f_nacimiento = datetime.datetime.strptime(request.POST.get('f_nacimiento', ''), "%Y-%m-%d").date()
            update.sexo = request.POST.get('sexo', '')
            update.e_civil = request.POST.get('e_civil', '')
            update.ocupacion = request.POST.get('ocupacion', '')
            update.religion = request.POST.get('religion', '')
            update.tipo_sanguinio = request.POST.get('tipo_sanguinio', '')
            update.domicilio = request.POST.get('domicilio', '')
            update.colonia = request.POST.get('colonia', '')
            update.cp = request.POST.get('cp', '')
            update.id_monedero = request.POST.get('id_monedero', '')
            update.mail = request.POST.get('mail', '')
            update.estado = request.POST.get('estado', '')
            update.municipio = request.POST.get('municipio', '')
            update.nopatologicos = request.POST.get('nopatologicos', '').upper()
            update.patologicos = request.POST.get('patologicos', '').upper()
            update.ginecologos = request.POST.get('ginecologos', '').upper()
            update.andrologicos = request.POST.get('andrologicos', '').upper()
            update.perinatales = request.POST.get('perinatales', '').upper()
            update.quirurgicos = request.POST.get('quirurgicos', '').upper()
            update.alergias = request.POST.get('alergias', '').upper()
            update.observaciones = request.POST.get('observaciones', '').upper()
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
    for tmp in properties.objects.all():
        propiedades = tmp
    return render(request,'patients_edit.html', {'patient':patient, 'propiedades':propiedades})

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

@login_required
def procedures (request):
    if request.method == 'GET':
        if request.GET.get('search') is not None:
            ListProcedures = Procedure.objects.filter(id__contains=request.GET.get('search').upper()).order_by('nombre')
            if len(ListProcedures) < 1:
                ListProcedures = Procedure.objects.filter(nombre__contains=request.GET.get('search').upper()).order_by('nombre')
        else:
            ListProcedures = Procedure.objects.all().order_by('nombre')

        paginator = Paginator(ListProcedures, 5) # Show 25 contacts per page

        page = request.GET.get('page')

        try:
            ListProcedures = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ListProcedures = paginator.page(1)
        except EmptyPage:
            # If page is out osf range (e.g. 9999), deliver last page of results.
            ListProcedures = paginator.page(paginator.num_pages)
        for tmp in properties.objects.all():
            propiedades = tmp
        return render(request,'procedures.html', {'ListProcedures':ListProcedures,'page_range':paginator.page_range,'count':paginator.num_pages, 'propiedades':propiedades})

    if request.method == 'POST':
        if request.POST.get('agendar') is not None:
                _agendar = True
        else:
            _agendar = False

        try:
            insert = Procedure(
            nombre = request.POST.get('nombre').upper(),
            descripcion = request.POST.get('descripcion').upper(),
            costo = request.POST.get('costo'),
            agendar = _agendar,
            monedero = request.POST.get('monedero')
            )
            insert.save()
            messages.success(request,'Procedimiento agregado')
        except Exception, e:
            messages.error(request,e)

        return redirect('/procedures')

@login_required
def procedures_Edit (request, id):
    if request.method == 'POST':
        if request.POST.get('agendar') is not None:
                _agendar = True
        else:
            _agendar = False

        try:
            update = Procedure.objects.get(id=id)
            update.nombre = request.POST.get('nombre').upper()
            update.descripcion = request.POST.get('descripcion').upper()
            update.costo = request.POST.get('costo')
            update.agendar = _agendar
            update.monedero = request.POST.get('monedero')
            update.save()
            messages.success(request, 'Procedimiento actualizado')
            return redirect ('/procedures')
        except Exception, e:
            messages.error(request, e)
            return redirect ('/procedures_edit/'+id)

    try:
        item = Procedure.objects.get(id= id)
    except Exception, e:
        messages.error(request,e)
    for tmp in properties.objects.all():
        propiedades = tmp
    return render(request,'procedure_edit.html', {'item':item, 'propiedades':propiedades})

@login_required
def procedure_Delete(request):
    if request.GET.get('id') is not None and request.user.is_superuser:
        try:
            p = Procedure.objects.get(id= request.GET.get('id'))
            p.delete()
            messages.success(request,'Procedimiento eliminado')
        except Exception, e:
            messages.error(request,e)

    return redirect('/procedures')


@login_required
def recipe(request):
    if request.method == 'GET':
        if request.GET.get('search') is not None:
            recetas = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(id__contains=request.GET.get('search').upper()).order_by('-f_consulta')
            if len(recetas) < 1:
                recetas = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(patient__nombre__contains=request.GET.get('search').upper()).order_by('-f_consulta')
            if len(recetas) < 1:
                recetas = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(patient__a_paterno__contains=request.GET.get('search').upper()).order_by('-f_consulta')
            if len(recetas) < 1:
                recetas = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(patient__a_materno__contains=request.GET.get('search').upper()).order_by('-f_consulta')
            if len(recetas) < 1:
                recetas = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(patient__id_monedero__contains=int(request.GET.get('search'))).order_by('-f_consulta')
        else:
            recetas = receta.objects.all().exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).order_by('-f_consulta')
        
        
        
        agenda = diary.objects.all().order_by('-id')

        paginator = Paginator(recetas, 10)
        page = request.GET.get('page')

        try:
            recetas = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            recetas = paginator.page(1)
        except EmptyPage:
            # If page is out osf range (e.g. 9999), deliver last page of results.
            recetas = paginator.page(paginator.num_pages)
        procedures = receta_procedures.objects.all()
        for tmp in properties.objects.all():
            propiedades = tmp
        return render(request,'recipe.html', {'recetas':recetas,'page_range':paginator.page_range,'count':paginator.num_pages,'procedures':procedures, 'agenda':agenda, 'propiedades':propiedades})

import time

@login_required
def consultation(request):
    if request.method == 'POST':
        id_paciente = request.POST.get('paciente')
        file0 = request.FILES.get('Archivo0', False)
        file1 = request.FILES.get('Archivo1', False)
        file2 = request.FILES.get('Archivo2', False)
        file3 = request.FILES.get('Archivo3', False)
        file4 = request.FILES.get('Archivo4', False)
        file5 = request.FILES.get('Archivo5', False)
        file6 = request.FILES.get('Archivo6', False)
        file7 = request.FILES.get('Archivo7', False)
        file8 = request.FILES.get('Archivo8', False)
        file9 = request.FILES.get('Archivo9', False)

        file0_url = ''
        file1_url = ''
        file2_url = ''
        file3_url = ''
        file4_url = ''
        file5_url = ''
        file6_url = ''
        file7_url = ''
        file8_url = ''
        file9_url = ''

        if  file0:
             var = file0
             ext = var.name.split(".")[-1]
             var.name = "0-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file0_url = fs.save(var.name, var)

        if  file1:
             var = file1
             ext = var.name.split(".")[-1]
             var.name = "1-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file1_url = fs.save(var.name, var)

        if  file2:
             var = file2
             ext = var.name.split(".")[-1]
             var.name = "2-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file2_url = fs.save(var.name, var)

        if  file3:
             var = file3
             ext = var.name.split(".")[-1]
             var.name = "3-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file3_url = fs.save(var.name, var)

        if  file4:
             var = file4
             ext = var.name.split(".")[-1]
             var.name = "4-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file4_url = fs.save(var.name, var)

        if  file5:
             var = file5
             ext = var.name.split(".")[-1]
             var.name = "5-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file5_url = fs.save(var.name, var)

        if  file6:
             var = file6
             ext = var.name.split(".")[-1]
             var.name = "6-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file6_url = fs.save(var.name, var)

        if  file7:
             var = file7
             ext = var.name.split(".")[-1]
             var.name = "7-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file7_url = fs.save(var.name, var)

        if  file8:
             var = file8
             ext = var.name.split(".")[-1]
             var.name = "8-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file8_url = fs.save(var.name, var)

        if  file9:
             var = file9
             ext = var.name.split(".")[-1]
             var.name = "9-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file9_url = fs.save(var.name, var)

        pp = patients.objects.get(id=request.POST.get('paciente'))
        
        
        share_r = False
        if pp.share:
            share_r = True

        r = receta(
                patient = patients.objects.get(id=request.POST.get('paciente')),
                edad = request.POST.get('edad'),
                temperatura = request.POST.get('temperatura'),
                peso = request.POST.get('peso'),
                cintura = request.POST.get('cintura'),
                estatura = request.POST.get('estatura'),
                presion_arterial = request.POST.get('presion_arterial'),
                imc = request.POST.get('imc'),
                exp_fisica = request.POST.get('exp_fisica'),
                extremidades = request.POST.get('extremidades'),
                p_actual = request.POST.get('p_actual'),
                torax = request.POST.get('torax'),
                abdomen = request.POST.get('abdomen'),
                genitales = request.POST.get('genitales'),
                piel = request.POST.get('piel'),
                diagnostico = request.POST.get('diagnostico'),
                pronostico = request.POST.get('pronostico'),
                terapeuticas = request.POST.get('terapeuticas'),
                f_consulta = str(datetime.datetime.now()),
                user = User.objects.get(id=request.user.id),
                total = request.POST.get('total_g'),
                indicaciones = request.POST.get('receta'),
                file0 = file0_url,
                file1 = file1_url,
                file2 = file2_url,
                file3 = file3_url,
                file4 = file4_url,
                file5 = file5_url,
                file6 = file6_url,
                file7 = file7_url,
                file8 = file8_url,
                file9 = file9_url,
                share = share_r
    			)
    	r.save()
        AddMondero = 0
        procedimientos = Procedure.objects.all().order_by('nombre')
        for a in procedimientos:
            if request.POST.get('p'+str(a.id)):
                p = receta_procedures(
                    receta = receta.objects.get(id=r.id),
                    procedure = Procedure.objects.get(id=a.id),
                    costo = a.costo
    			)
    	        p.save()
                AddMondero += Procedure.objects.get(id=a.id).monedero
        AddPtsMondero(AddMondero, request.POST.get('paciente'))

        if request.POST.get('use_monedero'):
            if r.patient.id_monedero == int(request.POST.get('id_monedero')):
                RemovePtsMondero(request.POST.get('total_g'), request.POST.get('paciente'))
                messages.success(request,'Consulta exitosa con descuento en monedero')
            else:
                messages.warning(request,'Consulta exitosa sin descuento en monedero')
        else:
                messages.success(request,'Consulta exitosa')

        return redirect ('/consultation/?recipe='+str(r.id))

    if request.method == 'GET':
        if request.user.is_superuser:
            Pacientes = patients.objects.all().exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).order_by('nombre')

            Procedures = Procedure.objects.all().order_by('nombre')
            Procedures_recipe = receta_procedures.objects.all()
            #recetas = receta.objects.all().order_by('f_consulta')

            for a in Pacientes:
                dt = datetime.datetime.now()
                year_actual = int(dt.strftime("%Y"))

                s = str(a.f_nacimiento)
                ss = s.split('-')

                if ss[0] != 'None':
                    year_nacimiento = int(ss[0])
                    a.f_nacimiento =  year_actual - year_nacimiento
            for tmp in properties.objects.all():
                propiedades = tmp
            return render(request, 'consultation.html', {'Pacientes':Pacientes, 'Procedures':Procedures, 'propiedades':propiedades, 'Procedures_recipe':Procedures_recipe})
        else:
            return redirect ('/manager')

def AddPtsMondero (pts, paciente):
    try:
        update = patients.objects.get(id=paciente)
        update.monedero = update.monedero + pts
        update.save()
    except Exception, e:
        print e

def RemovePtsMondero (pts, paciente):
    try:
        update = patients.objects.get(id=paciente)
        update.monedero = update.monedero - Decimal(pts)
        update.save()
    except Exception, e:
        print e

@login_required
def recipe_history(request, id):
    var = receta.objects.exclude(share=False, user__lt=request.user.id).exclude(share=False, user__gt=request.user.id).filter(patient__id__contains=id).order_by('-f_consulta')
    procedures = receta_procedures.objects.all()

    for tmp in properties.objects.all():
        propiedades = tmp
    return render(request,'recipe_history.html', {'var':var,'procedures':procedures, 'propiedades':propiedades})

@login_required
def diary_f(request):
    if request.method == 'POST':
        medic_select = User.objects.get(id=request.POST.get('medic'))
        d = diary(
            patient = patients.objects.get(id=request.POST.get('paciente')),
            receta = request.POST.get('receta'),
            f_start = request.POST.get('datetimepicker'),
            medic = medic_select
            )
        d.save()
        for tmp in properties.objects.all():
            propiedades = tmp
        body = 'NUEVA CITA CREADA CON EXITO. \n\nPACIENTE:' + d.patient.nombre +' '+ d.patient.a_paterno + ' ' +d.patient.a_materno
        body += '\nATENDERA: ' + medic_select.first_name.upper() +' '+ medic_select.last_name.upper()
        body +='\nFECHA: ' + d.f_start
        body += '\n\n' + propiedades.r_social
        body += '\nDIRECCION: ' + propiedades.direccion
        body += '\nTELEFONO: ' + propiedades.telefono
        body += '\n' + propiedades.lema.upper()
        email = EmailMessage('NUEVA CITA: ' + d.patient.nombre +' '+ d.patient.a_paterno + ' ' +d.patient.a_materno, body, to=[propiedades.correo+","+medic_select.email])
        email.send()

        messages.success(request,'Agregado')
        return redirect ('/diary')

    if request.method == 'GET':
        agenda = diary.objects.all()
        Pacientes = patients.objects.all().order_by('nombre')
        recetas =receta.objects.all().order_by('-f_consulta')
        medics = usuarios = User.objects.filter(is_superuser__contains=1)
        for tmp in properties.objects.all():
            propiedades = tmp
        return render(request,'diary.html', {'agenda':agenda, 'Pacientes':Pacientes, 'recetas':recetas, 'propiedades':propiedades, 'medics':medics})

@login_required
def consultation_agenda (request, id_agenda, id_paciente):
    if request.method == 'POST':
        file0 = request.FILES.get('Archivo0', False)
        file1 = request.FILES.get('Archivo1', False)
        file2 = request.FILES.get('Archivo2', False)
        file3 = request.FILES.get('Archivo3', False)
        file4 = request.FILES.get('Archivo4', False)
        file5 = request.FILES.get('Archivo5', False)
        file6 = request.FILES.get('Archivo6', False)
        file7 = request.FILES.get('Archivo7', False)
        file8 = request.FILES.get('Archivo8', False)
        file9 = request.FILES.get('Archivo9', False)

        file0_url = ''
        file1_url = ''
        file2_url = ''
        file3_url = ''
        file4_url = ''
        file5_url = ''
        file6_url = ''
        file7_url = ''
        file8_url = ''
        file9_url = ''

        if  file0:
             var = file0
             ext = var.name.split(".")[-1]
             var.name = "0-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file0_url = fs.save(var.name, var)

        if  file1:
             var = file1
             ext = var.name.split(".")[-1]
             var.name = "1-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file1_url = fs.save(var.name, var)

        if  file2:
             var = file2
             ext = var.name.split(".")[-1]
             var.name = "2-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file2_url = fs.save(var.name, var)

        if  file3:
             var = file3
             ext = var.name.split(".")[-1]
             var.name = "3-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file3_url = fs.save(var.name, var)

        if  file4:
             var = file4
             ext = var.name.split(".")[-1]
             var.name = "4-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file4_url = fs.save(var.name, var)

        if  file5:
             var = file5
             ext = var.name.split(".")[-1]
             var.name = "5-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file5_url = fs.save(var.name, var)

        if  file6:
             var = file6
             ext = var.name.split(".")[-1]
             var.name = "6-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file6_url = fs.save(var.name, var)

        if  file7:
             var = file7
             ext = var.name.split(".")[-1]
             var.name = "7-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file7_url = fs.save(var.name, var)

        if  file8:
             var = file8
             ext = var.name.split(".")[-1]
             var.name = "8-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file8_url = fs.save(var.name, var)

        if  file9:
             var = file9
             ext = var.name.split(".")[-1]
             var.name = "9-" + id_paciente + "_" + str(time.strftime("%d%m%y_%H%M%S")) +"." + ext
             fs = FileSystemStorage()
             file9_url = fs.save(var.name, var)

        r = receta(
                patient = patients.objects.get(id=request.POST.get('paciente')),
                edad = request.POST.get('edad'),
                temperatura = request.POST.get('temperatura'),
                peso = request.POST.get('peso'),
                cintura = request.POST.get('cintura'),
                estatura = request.POST.get('estatura'),
                presion_arterial = request.POST.get('presion_arterial'),
                imc = request.POST.get('imc'),
                exp_fisica = request.POST.get('exp_fisica'),
                extremidades = request.POST.get('extremidades'),
                p_actual = request.POST.get('p_actual'),
                torax = request.POST.get('torax'),
                abdomen = request.POST.get('abdomen'),
                genitales = request.POST.get('genitales'),
                piel = request.POST.get('piel'),
                diagnostico = request.POST.get('diagnostico'),
                pronostico = request.POST.get('pronostico'),
                terapeuticas = request.POST.get('terapeuticas'),
                f_consulta = str(datetime.datetime.now()),
                user = User.objects.get(id=request.user.id),
                total = request.POST.get('total_g'),
                indicaciones = request.POST.get('receta'),
                file0 = file0_url,
                file1 = file1_url,
                file2 = file2_url,
                file3 = file3_url,
                file4 = file4_url,
                file5 = file5_url,
                file6 = file6_url,
                file7 = file7_url,
                file8 = file8_url,
                file9 = file9_url
    			)
    	r.save()
        AddMondero = 0
        procedimientos = Procedure.objects.all().order_by('nombre')
        for a in procedimientos:
            if request.POST.get('p'+str(a.id)):
                p = receta_procedures(
                    receta = receta.objects.get(id=r.id),
                    procedure = Procedure.objects.get(id=a.id),
                    costo = a.costo
    			)
    	        p.save()
                AddMondero += Procedure.objects.get(id=a.id).monedero
        AddPtsMondero(AddMondero, request.POST.get('paciente'))
        agenda = diary.objects.get(id= id_agenda)
        agenda.delete()

        if request.POST.get('use_monedero'):
            if r.patient.id_monedero == int(request.POST.get('id_monedero')):
                RemovePtsMondero(request.POST.get('total_g'), request.POST.get('paciente'))
                messages.success(request,'Consulta exitosa con descuento en monedero')
            else:
                messages.warning(request,'Consulta exitosa sin descuento en monedero')
        else:
                messages.success(request,'Consulta exitosa')


        return redirect ('/consultation/?recipe='+str(r.id))

    if request.method == 'GET':
        if request.user.is_superuser:
            #Pacientes = patients.objects.all().order_by('nombre')
            Pacientes = patients.objects.all().exclude(share=False, medic__lt=request.user.id).exclude(share=False, medic__gt=request.user.id).order_by('nombre')
            Procedures = Procedure.objects.all().order_by('nombre')
            #Procedures_recipe = receta_procedures.objects.all()
            #recetas = receta.objects.all().order_by('f_consulta')

            for a in Pacientes:
                dt = datetime.datetime.now()
                year_actual = int(dt.strftime("%Y"))

                s = str(a.f_nacimiento)
                ss = s.split('-')

                if ss[0] != 'None':
                    year_nacimiento = int(ss[0])
                    a.f_nacimiento =  year_actual - year_nacimiento
            for tmp in properties.objects.all():
                propiedades = tmp
            return render(request, 'consultation_agenda.html', {'Pacientes':Pacientes, 'Procedures':Procedures, 'id_paciente':id_paciente, 'propiedades':propiedades})
        else:
            return redirect("/manager")

@login_required
def properties_update_ (request):
    if request.GET.get('propiedades_id') is not None:
        update = properties.objects.get(id=request.GET.get('propiedades_id'))
        update.r_social = request.GET.get('propiedades_razon_social')
        update.direccion = request.GET.get('propiedades_direccion')
        update.correo = request.GET.get('propiedades_correo')
        update.telefono = request.GET.get('propiedades_telefono')
        update.facebook = request.GET.get('propiedades_facebook')
        update.twitter = request.GET.get('propiedades_twitter')
        update.youtube = request.GET.get('propiedades_youtube')
        update.lema = request.GET.get('propiedades_lema')
        update.save()
    return redirect (request.GET.get('propiedades_url'))

@login_required
def profile_update (request):
    update = User.objects.get(id=request.user.id)
    update.first_name = request.GET.get('user_first_name')
    update.last_name = request.GET.get('user_last_name')
    update.email = request.GET.get('user_email')
    if request.GET.get('check_change_password') == 'on':
        if request.GET.get('password') == request.GET.get('password_confirm'):
            if len(request.GET.get('password')) > 0:
                update.set_password(request.GET.get('password'))
            else:
                messages.error(request, 'Ingrese un password')
        else:
            messages.error(request, 'El password no coincide')
    update.save()
    return redirect (request.GET.get('propiedades_url_perfil'))

@login_required
def _users (request):
    if request.GET.get('search') is not None:
        usuarios = User.objects.filter(first_name__contains=request.GET.get('search').upper()).order_by('-first_name')
        if len(usuarios) < 1:
            usuarios = User.objects.filter(last_name__contains=request.GET.get('search').upper()).order_by('-first_name')
    else:
        usuarios = User.objects.all()

    for tmp in properties.objects.all():
        propiedades = tmp
    return render(request, 'users.html', {'propiedades':propiedades, 'usuarios':usuarios})

@login_required
def _users_Delete(request):
    if request.GET.get('id') is not None and request.user.is_superuser:
        try:
            p = User.objects.get(id= request.GET.get('id'))
            p.delete()
            messages.success(request,'usuario eliminado')
        except Exception, e:
            messages.error(request,e)

    return redirect('/users')

@login_required
def _users_Update(request):
    _id = request.GET.get('id')
    if request.GET.get('check_change_medico'+_id) == 'on':
        medico = True
    else:
        medico = False

    if request.GET.get('check_change_asistente'+_id) == 'on':
        asistente = True
    else:
        asistente = False

    if request.GET.get('check_change_active'+_id) == 'on':
        active = True
    else:
        active = False

    update = User.objects.get(id=_id)
    update.first_name = request.GET.get('user_first_name')
    update.last_name = request.GET.get('user_last_name')
    update.email = request.GET.get('user_email')
    if request.GET.get('check_change_password'+str(_id)) == 'on':
        if request.GET.get('password'+str(_id)) == request.GET.get('password_confirm'+str(_id)):
            if len(request.GET.get('password'+str(_id))) > 0:
                update.set_password(request.GET.get('password'+str(_id)))
            else:
                messages.error(request, 'Ingrese un password')
        else:
            messages.error(request, 'El password no coincide')

    if medico:
        update.is_superuser = True
        update.is_staff = True

    if asistente:
        update.is_superuser = False
        update.is_staff = True

    if active:
        update.is_active = True
    else:
        update.is_active = False

    update.save()
    return redirect('/users')

@login_required
def _users_Add(request):
    try:
        if request.GET.get('add_medico') == 'on':
            medico = True
        else:
            medico = False

        r = User.objects.create_user(
                password = request.GET.get('password'),
                is_superuser = medico,
                first_name = request.GET.get('nombre'),
                last_name = request.GET.get('apellidos'),
                email = request.GET.get('email'),
                is_staff = True,
                is_active = True,
                username = request.GET.get('username')
                )
        r.save()
        messages.success(request, 'Usuario agregado')
    except Exception, e:
        messages.error(request, e)

    return redirect('/users')

@login_required
def recipe_receta (request, id):
    for tmp in properties.objects.all():
        propiedades = tmp

    _receta = receta.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='pro_LEFT', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_LEFT))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))
    data.append(Paragraph("| F. CONSULTA: " + str(_receta.f_consulta), styles['Normal']))
    data.append(Paragraph("| ATENDIO: " + _receta.user.first_name + _receta.user.last_name, styles['Normal']))
    data.append(Paragraph("| FOLIO RECETA: " + str(_receta.id), styles['Normal']))


    data.append(Paragraph("<br />| PACIENTE: " + _receta.patient.nombre + " " + _receta.patient.a_paterno + " " + _receta.patient.a_materno, styles['right_bold']))
    data.append(Paragraph("| EXPEDIENTE: " + _receta.patient.expediente + " | SEXO: " + _receta.patient.sexo + " | E. CIVIL: " + _receta.patient.e_civil, styles['right']))
    data.append(Paragraph("| TELEFONO: " + _receta.patient.telefono + " | CELULAR: " + _receta.patient.celular, styles['right']))
    data.append(Paragraph("| FECHA DE NACIMIENTO: " + str(_receta.patient.f_nacimiento) + "| EDAD: " + str(_receta.edad), styles['right']))
    data.append(Paragraph("| OCUPACION: " + _receta.patient.ocupacion, styles['right']))
    data.append(Paragraph("| RELIGION: " + _receta.patient.religion + " | TIPO SANGUINIO: " + _receta.patient.tipo_sanguinio + "<br />", styles['right']))

    data.append(Paragraph("<br />INFORMACION", styles['pro']))

    headings = ('TEMPERATURA', 'PESO', 'CINTURA', 'ESTATURA', 'PRESION ARTERIAL', 'IMC')
    allclientes = [(_receta.temperatura + " GRADOS",_receta.peso + " KGs", _receta.cintura + " CMs", _receta.estatura + "CMs",_receta.presion_arterial,_receta.imc)]

    t = Table([headings] + allclientes)
    data.append(t)

    if len(_receta.indicaciones) > 0:
        data.append(Paragraph("<br />RECETA E INDICACIONES", styles['pro']))
        data.append(Paragraph(_receta.indicaciones, styles['Normal']))

    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required
def recipe_consulta (request, id):
    for tmp in properties.objects.all():
        propiedades = tmp

    _receta = receta.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes_consulta.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='pro_LEFT', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_LEFT))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))
    data.append(Paragraph("| F. CONSULTA: " + str(_receta.f_consulta), styles['Normal']))
    data.append(Paragraph("| ATENDIO: " + _receta.user.first_name + _receta.user.last_name, styles['Normal']))
    data.append(Paragraph("| FOLIO RECETA: " + str(_receta.id), styles['Normal']))


    data.append(Paragraph("<br />| PACIENTE: " + _receta.patient.nombre + " " + _receta.patient.a_paterno + " " + _receta.patient.a_materno, styles['right_bold']))
    data.append(Paragraph("| EXPEDIENTE: " + _receta.patient.expediente + " | SEXO: " + _receta.patient.sexo + " | E. CIVIL: " + _receta.patient.e_civil, styles['right']))
    data.append(Paragraph("| TELEFONO: " + _receta.patient.telefono + " | CELULAR: " + _receta.patient.celular, styles['right']))
    data.append(Paragraph("| FECHA DE NACIMIENTO: " + str(_receta.patient.f_nacimiento) + "| EDAD: " + str(_receta.edad), styles['right']))
    data.append(Paragraph("| OCUPACION: " + _receta.patient.ocupacion, styles['right']))
    data.append(Paragraph("| RELIGION: " + _receta.patient.religion + " | TIPO SANGUINIO: " + _receta.patient.tipo_sanguinio + "<br />", styles['right']))

    data.append(Paragraph("<br />CONSULTA", styles['pro']))


    if len(_receta.exp_fisica) > 0:
        data.append(Paragraph("<br />| EXPLORACION FISICA", styles['pro_LEFT']))
        data.append(Paragraph(_receta.exp_fisica, styles['Normal']))

    if len(_receta.torax) > 0:
        data.append(Paragraph("<br />| TORAX", styles['pro_LEFT']))
        data.append(Paragraph(_receta.torax, styles['Normal']))

    if len(_receta.abdomen) > 0:
        data.append(Paragraph("<br />| ABDOMEN", styles['pro_LEFT']))
        data.append(Paragraph(_receta.abdomen, styles['Normal']))

    if len(_receta.genitales) > 0:
        data.append(Paragraph("<br />| GENITALES", styles['pro_LEFT']))
        data.append(Paragraph(_receta.genitales, styles['Normal']))

    if len(_receta.piel) > 0:
        data.append(Paragraph("<br />| PIEL", styles['pro_LEFT']))
        data.append(Paragraph(_receta.piel, styles['Normal']))

    if len(_receta.terapeuticas) > 0:
        data.append(Paragraph("<br />| RECOMENDACIONES TERAPEUTICAS", styles['pro_LEFT']))
        data.append(Paragraph(_receta.terapeuticas, styles['Normal']))

    if len(_receta.extremidades) > 0:
        data.append(Paragraph("<br />| EXTREMIDADES", styles['pro_LEFT']))
        data.append(Paragraph(_receta.extremidades, styles['Normal']))


    if len(_receta.diagnostico) > 0:
        data.append(Paragraph("<br />| DIAGNOSTICO", styles['pro_LEFT']))
        data.append(Paragraph(_receta.diagnostico, styles['Normal']))

    if len(_receta.p_actual) > 0:
        data.append(Paragraph("<br />| PADECIMIENTO ACTUAL", styles['pro_LEFT']))
        data.append(Paragraph(_receta.p_actual, styles['Normal']))

    if len(_receta.pronostico) > 0:
        data.append(Paragraph("<br />| PRONOSTICO", styles['pro_LEFT']))
        data.append(Paragraph(_receta.pronostico, styles['Normal']))

    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required
def _report_procedures (request):
    for tmp in properties.objects.all():
        propiedades = tmp


    response = HttpResponse(content_type='application/pdf')
    pdf_name = "procedimientos.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))

    data.append(Paragraph("<br />LISTA DE PROCEDIMIENTOS DISPONIBLES", styles['pro']))

    headings = ('FOLIO','PROCEDIMIENTO', 'COSTO','MONEDERO')
    allclientes = [(p.id, p.nombre, "$ " + str(p.costo), p.monedero) for p in Procedure.objects.all().order_by("nombre")]

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    data.append(t)

    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response


@login_required
def _report_patients (request):
    for tmp in properties.objects.all():
        propiedades = tmp


    response = HttpResponse(content_type='application/pdf')
    pdf_name = "pacientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))

    data.append(Paragraph("<br />LISTA DE PACIENTES EXISTENTES", styles['pro']))

    headings = ('EXPEDIENTE','NOMBRE', 'CELULAR', 'MONEDERO')
    allclientes = [(p.expediente, "(" + str(p.id) + ") " + p.nombre + " " + p.a_paterno + " " + p.a_materno, p.celular, p.monedero) for p in patients.objects.all().order_by("nombre")]

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    data.append(t)

    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response


@login_required
def _report_recipes (request):
    for tmp in properties.objects.all():
        propiedades = tmp


    response = HttpResponse(content_type='application/pdf')
    pdf_name = "pacientes.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))

    data.append(Paragraph("<br />LISTA DE RECETAS EXPEDIDAS", styles['pro']))

    headings = ('FOLIO','PACIENTE', 'TOTAL', 'F. CONSULTA')
    allclientes = [(p.id, "(" + str(p.patient.id) + ") " + p.patient.nombre + " " + p.patient.a_paterno + " " + p.patient.a_materno, str(p.total) + " MXN", p.f_consulta) for p in receta.objects.all().order_by("-f_consulta")]

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    data.append(t)

    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required
def report_heredofamiliares (request, id):
    for tmp in properties.objects.all():
        propiedades = tmp

    _receta = patients.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "historia_clinica.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='pro_LEFT', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_LEFT))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))
    data.append(Paragraph("| PACIENTE: " + _receta.nombre  + " " +_receta.a_paterno + " " + _receta.a_materno, styles['Normal']))
    header = Paragraph("HISTORIA CLINICA", styles['Title'])
    data.append(header)

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />NO PATOLOGICOS", styles['pro']))
        data.append(Paragraph(_receta.nopatologicos, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />PATOLOGICOS", styles['pro']))
        data.append(Paragraph(_receta.patologicos, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />GINECOLOGOS", styles['pro']))
        data.append(Paragraph(_receta.ginecologos, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />ANDROLOGICOS", styles['pro']))
        data.append(Paragraph(_receta.andrologicos, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />PERINATALES", styles['pro']))
        data.append(Paragraph(_receta.perinatales, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />QUIRURGICOS", styles['pro']))
        data.append(Paragraph(_receta.quirurgicos, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />ALERGIAS", styles['pro']))
        data.append(Paragraph(_receta.alergias, styles['Normal']))

    if len(_receta.nopatologicos) > 0:
        data.append(Paragraph("<br />PADECIMIENTO ACTUAL", styles['pro']))
        data.append(Paragraph(_receta.observaciones, styles['Normal']))

    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required
def report_datos_paciente (request, id):
    for tmp in properties.objects.all():
        propiedades = tmp

    _receta = patients.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    pdf_name = "historia_clinica.pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=10,
                            topMargin=10,
                            bottomMargin=10,
                            )
    data = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='right', fontName = 'Helvetica', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='right_bold', fontName = 'Helvetica-bold', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='pro', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='pro_LEFT', fontSize=10, fontName = 'Helvetica-bold', alignment=TA_LEFT))


    header = Paragraph(propiedades.r_social, styles['Title'])
    data.append(header)
    data.append(Paragraph("| DIRECCION: " + propiedades.direccion, styles['Normal']))
    data.append(Paragraph("| CORREO ELECTRONICO: " + propiedades.correo, styles['Normal']))
    data.append(Paragraph("| TELEFONO: " + propiedades.telefono, styles['Normal']))
    data.append(Paragraph("| PACIENTE: " + _receta.nombre  + " " +_receta.a_paterno + " " + _receta.a_materno, styles['Normal']))
    header = Paragraph("DATOS PERSONALES", styles['Title'])
    data.append(header)

    data.append(Paragraph("<br />NO. DE EXPEDIENTE", styles['pro']))
    data.append(Paragraph(_receta.expediente, styles['Normal']))

    data.append(Paragraph("<br />TELEFONO", styles['pro']))
    data.append(Paragraph(_receta.telefono, styles['Normal']))

    data.append(Paragraph("<br />CELULAR", styles['pro']))
    data.append(Paragraph(_receta.celular, styles['Normal']))

    data.append(Paragraph("<br />SEXO", styles['pro']))
    data.append(Paragraph(_receta.sexo, styles['Normal']))

    data.append(Paragraph("<br />ESTADO CIVIL", styles['pro']))
    data.append(Paragraph(_receta.e_civil, styles['Normal']))

    data.append(Paragraph("<br />OCUPACION", styles['pro']))
    data.append(Paragraph(_receta.ocupacion, styles['Normal']))

    data.append(Paragraph("<br />RELIGION", styles['pro']))
    data.append(Paragraph(_receta.religion, styles['Normal']))

    data.append(Paragraph("<br />TIPO SANGUINEO", styles['pro']))
    data.append(Paragraph(_receta.tipo_sanguinio, styles['Normal']))

    data.append(Paragraph("<br />DOMICLIO", styles['pro']))
    data.append(Paragraph(_receta.domicilio + _receta.colonia + ", "+ _receta.municipio + ", " + _receta.estado, styles['Normal']))

    data.append(Paragraph("<br />CORREO ELECTRONICO", styles['pro']))
    data.append(Paragraph(_receta.mail, styles['Normal']))

    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("", styles['Normal']))
    data.append(Paragraph("<br />www.cyberchoapas.com", styles['pro']))
    doc.build(data)
    response.write(buff.getvalue())
    buff.close()
    return response

@login_required
def delete_recipe(request):
    if request.GET.get('id') is not None and request.user.is_superuser:
        try:
            p = receta.objects.get(id= request.GET.get('id'))
            p.delete()
            messages.success(request,'Receta eliminada')
        except Exception, e:
            messages.error(request,e)

    return redirect('/recipe')

@login_required
def delete_recipe_history(request):
    if request.GET.get('id') is not None and request.user.is_superuser:
        try:
            p = receta.objects.get(id= request.GET.get('id'))
            p.delete()
            messages.success(request,'Receta eliminada')
            return redirect('/recipe_history/'+request.GET.get('client'))
        except Exception, e:
            messages.error(request,e)

    return redirect('/recipe_history/'+request.GET.get('client'))

@login_required
def shareyes_recipe (request):
    try:
        update = receta.objects.get(id=request.GET.get('id'))
        update.share = True
        update.save()
        messages.success(request, 'Receta compartida con exito')
        return redirect ('/recipe')
    except Exception, e:
        messages.error(request, e)
        return redirect ('/recipe')

@login_required
def shareno_recipe (request):
    try:
        update = receta.objects.get(id=request.GET.get('id'))
        update.share = False
        update.save()
        messages.success(request, 'Receta NO compartida con exito')
        return redirect ('/recipe')
    except Exception, e:
        messages.error(request, e)
        return redirect ('/recipe')

@login_required
def shareyes_paciente (request):
    try:
        update = patients.objects.get(id=request.GET.get('id'))
        update.share = True
        update.save()
        messages.success(request, 'Paciente compartido con exito')
        return redirect ('/patient')
    except Exception, e:
        messages.error(request, e)
        return redirect ('/patient')

@login_required
def shareno_paciente (request):
    try:
        update = patients.objects.get(id=request.GET.get('id'))
        update.share = False
        update.save()
        messages.success(request, 'Paciente NO compartido con exito')
        return redirect ('/patient')
    except Exception, e:
        messages.error(request, e)
        return redirect ('/patient')