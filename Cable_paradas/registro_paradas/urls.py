from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Pestaña detenciones
    path('create/', views.create_event, name='create_record'),
    path('record/update/<pk>', views.update_detenciones, name='update_detencion'),
    path('list_of_stops/', views.list_of_events, name='list_of_stop'),
    path('grafico/', views.grafico_datos, name='grafico_datos'),
    path('reports_stops/', views.generate_report, name='report_stop'),
    path('load_stop_codes/', views.load_stop_codes, name='load_stop_codes'),

    # Pestaña registro de operacion
    path('create_transaction_record/', views.operating_day, name='create_transaction_record'),
    path('list_of_operational/', views.operational_day_list, name='list_of_operational'),
    path('report_operation/', views.generate_report_operation_day, name='report_operation'),
    path('transaction_record/update/<pk>', views.update_operation_day, name='record_update'),

    # Pestaña datos tecnicos
    path('create_technical_data/', views.create_technical_data, name='create_technical_data'),
    path('list_technical_data/', views.technical_data_list, name='list_technical_data'),
    path('report_technical_data', views.generate_report_technical_data, name='report_technical_data'),
]
