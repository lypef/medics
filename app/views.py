from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.contrib.auth.models import User
from models import patients, Procedure, receta, receta_procedures, diary, properties
from reportlab.pdfgen import canvas
from django.http import HttpResponse

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
            ListPatients = patients.objects.filter(nombre__contains=request.GET.get('search').upper()).order_by('nombre')
        else:
            ListPatients = patients.objects.all().order_by('nombre')

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
                mail = request.POST.get('mail', ''),
                estado = request.POST.get('estado', ''),
                municipio = request.POST.get('municipio', ''),
                heredados = request.POST.get('heredados', '').upper(),
                nopatologicos = request.POST.get('nopatologicos', '').upper(),
                patologicos = request.POST.get('patologicos', '').upper(),
                ginecologos = request.POST.get('ginecologos', '').upper(),
                andrologicos = request.POST.get('andrologicos', '').upper(),
                perinatales = request.POST.get('perinatales', '').upper(),
                quirurgicos = request.POST.get('quirurgicos', '').upper(),
                alergias = request.POST.get('alergias', '').upper(),
                observaciones = request.POST.get('observaciones', '').upper()
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
            update.mail = request.POST.get('mail', '')
            update.estado = request.POST.get('estado', '')
            update.municipio = request.POST.get('municipio', '')
            update.heredados = request.POST.get('heredados', '').upper()
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
            agendar = _agendar
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
            recetas = receta.objects.filter(patient__nombre__contains=request.GET.get('search').upper()).order_by('-f_consulta')
        else:
            recetas = receta.objects.all().order_by('-f_consulta')

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

@login_required
def consultation(request):
    if request.method == 'POST':
        print request.POST.get('paciente')
        r = receta(
                patient = patients.objects.get(id=request.POST.get('paciente')),
                edad = request.POST.get('edad'),
                temperatura = request.POST.get('temperatura'),
                peso = request.POST.get('peso'),
                estatura = request.POST.get('estatura'),
                presion_arterial = request.POST.get('presion_arterial'),
                talla = request.POST.get('talla'),
                imc = request.POST.get('imc'),
                cabeza = request.POST.get('cabeza'),
                torax = request.POST.get('torax'),
                abdomen = request.POST.get('abdomen'),
                genitales = request.POST.get('genitales'),
                piel = request.POST.get('piel'),
                diagnostico = request.POST.get('diagnostico'),
                pronostico = request.POST.get('pronostico'),
                terapeuticas = request.POST.get('terapeuticas'),
                f_consulta = str(datetime.datetime.now()),
                user = User.objects.get(id=request.user.id),
                total = request.POST.get('total_g')
    			)
    	r.save()
        procedimientos = Procedure.objects.all().order_by('nombre')
        for a in procedimientos:
            if request.POST.get('p'+str(a.id)):
                p = receta_procedures(
                    receta = receta.objects.get(id=r.id),
                    procedure = Procedure.objects.get(id=a.id),
                    costo = a.costo
    			)
    	        p.save()
        messages.success(request,'Consulta exitosa')
        return redirect ('/consultation')

    if request.method == 'GET':
        Pacientes = patients.objects.all().order_by('nombre')
        Procedures = Procedure.objects.all().order_by('nombre')

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
        return render(request, 'consultation.html', {'Pacientes':Pacientes, 'Procedures':Procedures, 'propiedades':propiedades})

@login_required
def recipe_history(request, id):
    var = receta.objects.filter(patient__id__contains=id).order_by('-f_consulta')
    procedures = receta_procedures.objects.all()

    for tmp in properties.objects.all():
        propiedades = tmp
    return render(request,'recipe_history.html', {'var':var,'procedures':procedures, 'propiedades':propiedades})

@login_required
def diary_f(request):
    if request.method == 'POST':
        d = diary(
            patient = patients.objects.get(id=request.POST.get('paciente')),
            receta = request.POST.get('receta'),
            f_start = request.POST.get('datetimepicker')
            )
        d.save()



        messages.success(request,'Agregado')
        return redirect ('/diary')

    if request.method == 'GET':
        agenda = diary.objects.all()
        Pacientes = patients.objects.all().order_by('nombre')
        recetas =receta.objects.all().order_by('-f_consulta')
        for tmp in properties.objects.all():
            propiedades = tmp
        return render(request,'diary.html', {'agenda':agenda, 'Pacientes':Pacientes, 'recetas':recetas, 'propiedades':propiedades})

@login_required
def consultation_agenda (request, id_agenda, id_paciente):
    if request.method == 'POST':
        r = receta(
                patient = patients.objects.get(id=request.POST.get('paciente')),
                edad = request.POST.get('edad'),
                temperatura = request.POST.get('temperatura'),
                peso = request.POST.get('peso'),
                estatura = request.POST.get('estatura'),
                presion_arterial = request.POST.get('presion_arterial'),
                talla = request.POST.get('talla'),
                imc = request.POST.get('imc'),
                cabeza = request.POST.get('cabeza'),
                torax = request.POST.get('torax'),
                abdomen = request.POST.get('abdomen'),
                genitales = request.POST.get('genitales'),
                piel = request.POST.get('piel'),
                diagnostico = request.POST.get('diagnostico'),
                pronostico = request.POST.get('pronostico'),
                terapeuticas = request.POST.get('terapeuticas'),
                f_consulta = str(datetime.datetime.now()),
                user = User.objects.get(id=request.user.id),
                total = request.POST.get('total_g')
    			)
    	r.save()
        procedimientos = Procedure.objects.all().order_by('nombre')
        for a in procedimientos:
            if request.POST.get('p'+str(a.id)):
                p = receta_procedures(
                    receta = receta.objects.get(id=r.id),
                    procedure = Procedure.objects.get(id=a.id),
                    costo = a.costo
    			)
    	        p.save()
        agenda = diary.objects.get(id= id_agenda)
        agenda.delete()
        messages.success(request,'Consulta exitosa')
        return redirect ('/consultation')

    if request.method == 'GET':
        Pacientes = patients.objects.all().order_by('nombre')
        Procedures = Procedure.objects.all().order_by('nombre')

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

def recipe_receta (request, id):
    for tmp in properties.objects.all():
        propiedades = tmp

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 800, propiedades.r_social)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
