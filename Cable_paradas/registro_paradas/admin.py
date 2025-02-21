from django.contrib import admin
from .models import *

admin.site.register(StopCode)
admin.site.register(Station)
admin.site.register(Cabin)
admin.site.register(Cabin2)
admin.site.register(Shift)
admin.site.register(OperationTime)
admin.site.register(TechnicalData)
admin.site.register(EventType)
admin.site.register(Evacuacion)


class StopRegister(admin.ModelAdmin):
    list_display = (  'stop_code','station', 'start_date', 'end_date',
                    'stop_time', 'observation')
    readonly_fields = ('stop_time',)

admin.site.register(StopRegistration, StopRegister)


class EventStopCodeAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'content_type', 'related_object')
    list_filter = ('event_type',)

admin.site.register(EventStopCode, EventStopCodeAdmin)