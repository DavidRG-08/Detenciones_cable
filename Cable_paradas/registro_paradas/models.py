from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User 
from datetime import datetime, timedelta
from django.db import models

class StopCode(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=70)
    
    def __str__(self):
        return f"{self.code}" + " -- " + f"{self.description}"
    

class Station(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.name}"
    

class Cabin(models.Model):
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.code}"


class Cabin2(models.Model):
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.code}"
    

class Shift(models.Model):
    code_turn = models.CharField(max_length=1)
    
    def __str__(self):
        return f"{self.code_turn}"


class EventType(models.Model):
    name_event = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name_event}"


class StopRegistration(models.Model):
    registration_date = models.DateField()
    stop_code = models.CharField(max_length=255, null=True, blank=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    start_date = models.TimeField()
    end_date = models.TimeField()
    stop_time = models.IntegerField()
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE, null=True, blank=True)
    cabin2 = models.ForeignKey(Cabin2, on_delete=models.CASCADE, null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    observation = models.TextField(null=True)
    inputable = models.CharField(max_length=10, default=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True)
    
    def save(self, *args, **kwargs):
        # definir si es inputable
        if self.event_type and self.event_type.name_event == "Tormenta electrica":
            self.inputable = False
        
        #Calcular duracion en segundos
        if self.end_date and self.start_date:
            start_datetime =  datetime.combine(datetime.min, self.start_date)
            end_datetime = datetime.combine(datetime.min, self.end_date)
            
            # Si end_date es menor que start_date, asumimos que cruza la medianoche
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)
            
            delta = end_datetime - start_datetime
            self.stop_time = int(delta.total_seconds())
        
        else:
            self.stop_time = 0
            
        super().save(*args, **kwargs)
        
        
        # #calcular duracion en segundos
        # if self.end_date and self.start_date:
        #     delta = self.end_date - self.start_date
        #     # self.stop_time = int(delta.total_seconds()/60)
        #     self.stop_time = int(delta.total_seconds())
        # else:
        #     self.stop_time = 0
        # super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.registration_date}" + " -- " +f"{self.stop_code}"
    
class Evacuacion(models.Model):
    event_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.event_name}"
    
    
class Detentions(models.Model):
    detention_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.detention_name}"
    

class SpeedChange(models.Model):
    speed_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.speed_name}"
    


class EventStopCode(models.Model):
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)

    # Campos para manejar las relaciones genericas
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    related_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = ('event_type', 'content_type','object_id')
    
    def __str__(self):
        return f"{self.event_type} - {self.related_object}"
    

class OperationTime(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    horometer_start = models.DecimalField(max_digits=10, decimal_places=2)
    end_time = models.TimeField(blank=True, null=True)
    horometer_end = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    total_time = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        #Calcular duracion si ambos campos estan completos
        if self.start_time and self.end_time:
            start_datetime =  datetime.combine(datetime.min, self.start_time)
            end_datetime = datetime.combine(datetime.min, self.end_time)
            
            # Si end_date es menor que start_date, asumimos que cruza la medianoche
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)
            
            delta = end_datetime - start_datetime
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            self.total_time = f"{hours}: {minutes:02d}"
        else:
            self.total_time = None
            
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.date}"
