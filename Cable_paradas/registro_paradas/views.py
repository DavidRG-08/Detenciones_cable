from .forms import FormRegister, LoginForm, RegistroForm, FormOperatingDay
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StopRegistration, EventStopCode, OperationTime
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .reports import ReporterExcelStop, ReporterExcelOperatorDay
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from datetime import datetime
import logging

logger = logging.getLogger('registro_paradas')


# da acceso a la aplicacion
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Nombre de usuario o clave incorrectos')
                    
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

# salir de la aplicacion
def logout_view(request):
    logout(request)
    return redirect('login')

# Pagina principal
@login_required
def home(request):
    context = {
        "Fecha_hora": datetime.now(),
        "Paradas": StopRegistration.objects.all(),
        "Paradas_dia": StopRegistration.objects.filter(registration_date = datetime.now().strftime("%Y-%m-%d")),
        "paradas_station": StopRegistration.objects.filter(station=1),
        "paradas_station2": StopRegistration.objects.filter(station=2),
        "paradas_station3": StopRegistration.objects.filter(station=3),
        "paradas_station4": StopRegistration.objects.filter(station=4),
        "paradas_station5": StopRegistration.objects.filter(station=5),
        "tipo_evento1": StopRegistration.objects.filter(event_type=1),
        "tipo_evento2": StopRegistration.objects.filter(event_type=2),
        "tipo_evento3": StopRegistration.objects.filter(event_type=3),
        "tipo_evento4": StopRegistration.objects.filter(event_type=4),
    }
    
    return render(request, 'registro_paradas/index.html', context)


# Crear y registrar usuarios 
@login_required
def view_register(request):
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if user_form.is_valid():
            # Crea y guarda el usuario
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Usuario creado')

            return redirect('register_user')
        else:
            messages.error(request, 'Hubo un error al crear el usuario.')
    else:
        user_form = RegistroForm()
        
    
    return render(request, 'registration/register_user.html', {'user_form': user_form})


# Crea el evento de parada
@login_required
def create_event(request):
    if request.method == 'POST':
        form = FormRegister(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.operator = request.user
            #calcular la duracion antes de guardar
            register.save()
            messages.success(request, 'Evento creado correctamente')
            return redirect('create_record')
        else:
            messages.error(request, 'Hubo un error al registrar el evento, validar la informacion ingresada')
    else:
        form = FormRegister()
    
    return render(request, 'registro_paradas/create_record.html', {'form': form})
    
    
# # Accede al listado de eventos registrados
@login_required
def list_of_events(request):
    # Obtiene todos los registros del modelo
    registros = StopRegistration.objects.all().order_by('-registration_date', '-start_date')
    
    # rango de fechas
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # filtro en un rango de fechas
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            registros = registros.filter(
                registration_date__gte = start_date, 
                registration_date__lte = end_date
            )
        except ValueError:
            pass
    
    # Procesa cada registro    
    for registro in registros:
        try:
            # Obtiene el EventStopCode correspondiente
            stop_code_obj = EventStopCode.objects.get(
                event_type = registro.event_type,
                object_id = registro.stop_code
            )
            
            # Usa el content_type del objeto para obtener el modelo relacionado
            content_type = stop_code_obj.content_type
            related_object = content_type.get_object_for_this_type(pk=stop_code_obj.object_id)
            
            # verificar dinamicamente si el objeto relacionado tiene un campo 'code', 'event_name', 'detention_name', 'speed_name'
            if hasattr(related_object, 'description'):
                registro.stop_code_name = related_object.code
            elif hasattr(related_object, 'event_name'):
                registro.stop_code_name = related_object.event_name
            elif hasattr(related_object, 'detention_name'):
                registro.stop_code_name = related_object.detention_name
            elif hasattr(related_object, 'speed_name'):
                registro.stop_code_name = related_object.speed_name
            else:
                registro.stop_code_name = "Nombre no encontrado"
            
        except EventStopCode.DoesNotExist:
            registro.stop_code_name = "Code no found"
        
        
    
    # agrega el paginador
    paginator = Paginator(registros, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'registro_paradas/list_stop.html', {'page_obj': page_obj})


# VIsta para acceder a dashboard creados en power BI
@login_required
def grafico_datos(request):
    return render(request, 'registro_paradas/grafico.html')


# Vista para descargar el reporte en excel de detenciones
@login_required
def generate_report(request):
    # Obtener los filtros de fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Parsear las fechas usando parse_date para convertir de string a date
    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)
    
    print(f"Start date: {start_date}, End Date: {end_date}")
    
    # Consulta para filtrar los registros
    queryset = StopRegistration.objects.all()
    if start_date and end_date:
        queryset = queryset.filter(registration_date__gte = start_date, registration_date__lte = end_date)
        
    # Generar el reporte solo con los registros filtrados
    report = ReporterExcelStop(queryset)
    return report.get(request)


# VIsta para cargar las opciones por evento
@login_required
def load_stop_codes(request):
    event_type_id = request.GET.get('event_type_id')
    
    if event_type_id:
        event_stop_codes = EventStopCode.objects.filter(event_type_id=event_type_id)
        stop_code_list = []
        
        for esc in event_stop_codes:
            obj = esc.related_object # Obtiene el objeto relacionado
            
            if hasattr(obj, 'code'):
                stop_code_list.append({'id': obj.id, 'name': obj.code + " - " + obj.description})
            if hasattr(obj, 'event_name'):
                stop_code_list.append({'id': obj.id, 'name': obj.event_name})
            elif hasattr(obj, 'detention_name'):
                stop_code_list.append({'id': obj.id, 'name': obj.detention_name})
            elif hasattr(obj, 'speed_name'):
                stop_code_list.append({'id': obj.id, 'name': obj.speed_name})
        
        return JsonResponse(stop_code_list, safe=False)
    
    return JsonResponse({'error': 'Invalid event_type'}, status=400)


# Vista para registrar la hora de inicio y fin de la operacion
@login_required
def operating_day(request):
    if request.method == 'POST':
        form = FormOperatingDay(request.POST)
        if form.is_valid():
            register = form.save(commit=False)
            register.operator = request.user
            form.save()
            messages.success(request, 'Registro creado correctamente')
            return redirect('create_transaction_record')
        else:
            messages.error(request, 'Hubo un error al momento de insertar el registro, valide nuevamente la informacion')
    else:
        form = FormOperatingDay()
    
    return render(request, 'registro_paradas/create_transaction_record.html', {'form': form})


@login_required
def operational_day_list(request):
    records = OperationTime.objects.all().order_by('-date')

    # Rango de fechas
    start_date_op = request.GET.get('start_date_op')
    end_date_op = request.GET.get('end_date_op')

    if start_date_op and end_date_op:
        try:
            start_date_op = datetime.strptime(start_date_op, '%Y-%m-%d').date()
            end_date_op = datetime.strptime(end_date_op, '%Y-%m-%d').date()

            records = records.filter(
                date__gte = start_date_op,
                date__lte = end_date_op
            )
        except ValueError:
            pass
    

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj_ope = paginator.get_page(page_number)

    return render(request, 'registro_paradas/list_operational_day.html', {'page_obj_ope': page_obj_ope})


# Vista para descargar el reporte en excel de detenciones
@login_required
def generate_report_operation_day(request):
    # Obtener los filtros de fecha
    start_date_op = request.GET.get('start_date_op')
    end_date_op = request.GET.get('end_date_op')
    
    # Parsear las fechas usando parse_date para convertir de string a date
    if start_date_op:
        start_date_op = parse_date(start_date_op)
    if end_date_op:
        end_date_op = parse_date(end_date_op)
    
    print(f"Start date: {start_date_op}, End Date: {end_date_op}")
    
    # Consulta para filtrar los registros
    queryset = OperationTime.objects.all()
    if start_date_op and end_date_op:
        queryset = queryset.filter(date__gte = start_date_op, date__lte = end_date_op)
        
    # Generar el reporte solo con los registros filtrados
    report = ReporterExcelOperatorDay(queryset)
    return report.get(request)


def update_operation_day(request, pk):
    instancia = get_object_or_404(OperationTime, pk=pk)
    if request.method == 'POST':
        form = FormOperatingDay(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            return redirect('list_of_operational')  # URL redireccion success
    
    else:
        form = FormOperatingDay(instance=instancia)
    
    return render(request, 'registro_paradas/update_operation_day.html', {'form': form})
