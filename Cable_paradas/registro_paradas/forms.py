from django.contrib.auth.models import User
from .models import StopRegistration, OperationTime, TechnicalData
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class FormRegister(forms.ModelForm):    
    class Meta:
        model = StopRegistration
        fields = [
            'event_type',
            'registration_date',
            'stop_code',
            'station', 
            'start_date', 
            'end_date', 
            'cabin',
            'cabin2',
            'shift',
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
        


class FormRegisterUpdate(forms.ModelForm):    
    class Meta:
        model = StopRegistration
        fields = [
            'registration_date',
            'station', 
            'start_date', 
            'end_date', 
        ]
        
        labels = {
            "registration_date": "Fecha de registro",
            "station": "Estacion",
            "start_date": "Hora de parada",
            "end_date": "Hora inicio de operacion",
        }
        
        widgets = {
            'registration_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1}),
            'end_date': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1})
        }
        
            
        
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


class FormTechnicalData(forms.ModelForm):
    class Meta:
        model = TechnicalData
        fields = ["date", "time", "temp_motor_variador", "temp_cuarto_variador", "temp_reductor", "temp_reductor_panel", "par", "presion_fs_bar", "presion_fe_bar", "carro_tensor_tunal",
                  "carro_tensor_paraiso", "longitud_de_linea", "viento_p06", "viento_p16", "viento_p23"]
        labels = {
            "date": "Fecha", 
            "time": "Hora",
            "temp_motor_variador": "Temp motor variador",
            "temp_cuarto_variador": "Temp cuarto variador",
            "temp_reductor": "Temp reductor",
            "temp_reductor_panel": "Temp reductor panel (°C)",
            "par": "Par (%)",
            "presion_fs_bar": "Presion fs bar",
            "presion_fe_bar": "Presion fe bar",
            "carro_tensor_tunal": "Carro tensor tunal",
            "carro_tensor_paraiso": "Carro tensor paraiso",
            "longitud_de_linea": "Longitud de linea (pulsos)",
            "viento_p06": "Viento p06 (m/s)",
            "viento_p16": "Viento p16 (m/s)",
            "viento_p23": "Viento p23 (m/s)",
        }
    

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': 1}),
            'temp_motor_variador': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'temp_cuarto_variador': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'temp_reductor': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'temp_reductor_panel': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'par': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'presion_fs_bar': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'presion_fe_bar': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'carro_tensor_tunal': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'carro_tensor_paraiso': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'longitud_de_linea': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'viento_p06': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'viento_p16': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'viento_p23': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
        }