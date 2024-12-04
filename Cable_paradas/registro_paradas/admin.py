from django.contrib import admin
from .models import Station, Cabin, Shift, StopRegistration, EventStopCode, StopCode, OperationTime

admin.site.register(StopCode)
admin.site.register(Station)
admin.site.register(Cabin)
admin.site.register(Shift)
admin.site.register(OperationTime)


class StopRegister(admin.ModelAdmin):
    list_display = (  'stop_code','station', 'start_date', 'end_date',
                    'stop_time', 'observation')
    readonly_fields = ('stop_time',)

admin.site.register(StopRegistration, StopRegister)


class EventStopCodeAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'content_type', 'related_object')
    list_filter = ('event_type',)

admin.site.register(EventStopCode, EventStopCodeAdmin)