from django.contrib.auth.models import User
from .models import StopRegistration, OperationTime
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Contraseña")
    
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'username', 'email', 'password']
        
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellido",
            "username": "Usuario",
            "email": "correo electronico",
            "password": "Contraseña",
        }
        
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese su correo'
                }),
        }

    
class FormRegister(forms.ModelForm):
    
    
    class Meta:
        model = StopRegistration
        fields = [
            'registration_date',
            'stop_code',
            'station', 
            'start_date', 
            'end_date', 
            'cabin',
            'cabin2',
            'shift',
            'event_type',
            'observation',
        ]
        
        labels = {
            "registration_date": "Fecha de registro",
            "stop_code": "Motivo de parada",
            "station": "Estacion",
            "start_date": "Hora de parada",
            "end_date": "Hora inicio de operacion",
            "cabin": "Cabina 1",
            "cabin2": "Cabina 2",
            "shift": "Turno",
            "event_type": "Tipo de evento",
            "observation": "Observaciones",
        }
        
        widgets = {
            'stop_code': forms.Select(attrs={'class': 'form-control select2'}),
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1}),
            'end_date': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1})
        }
        
        def clean(self):
            cleaned_data = super().clean()
            event_type = cleaned_data.get("event_type")
            
            if event_type and event_type.name_event == 'Tormenta electrica':
                cleaned_data['inputable'] = 'False'
            else:
                cleaned_data['inputable'] = True
                
            return cleaned_data
        
        
class FormOperatingDay(forms.ModelForm):
    class Meta:
        model = OperationTime
        fields = ['date','start_time','horometer_start','end_time','horometer_end']

        labels = {
            "date": "Fecha",
            "start_time": "Hora Inicio", 
            "horometer_start": "Horometro inicio operacion",
            "end_time": "Hora Fin",
            "horometer_end": "Horometro fin operacion"
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1}),
            'horometer_start': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Ingrese el horómetro inicial','class': 'form-control'}),
            'horometer_end': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Ingrese el horómetro final','class': 'form-control'})
        }