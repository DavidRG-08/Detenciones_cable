from django.views.generic import TemplateView
from django.http.response import HttpResponse
from .models import StopRegistration, OperationTime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

class ReporterExcelStop(TemplateView):
    def __init__(self, queryset = None):
        # Utiliza el queryset pasado en el constructor o todos los registros si no se pasa
        self.queryset = queryset or StopRegistration.objects.all()
    
    def get(self, request, *args, **kwargs):
        # Aqui utilizamos el queryset filtrado en lugar de obtener todos los registros
        stop_reg = self.queryset        
        
        # Crea el archivo excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Paradas Registradas"
        
        # Estilos
        title_font = Font(bold=True, size=14)
        header_font = Font(bold=True)
        header_fill = PatternFill(start_color="13678A", end_color="13678A", fill_type="solid")
        center_alignment = Alignment(horizontal="center")
        
        ws["A1"] = "REPORTE PARADAS REGISTRADAS"
        ws.merge_cells("A1:M1")
        ws["A1"].font = title_font
        ws["A1"].alignment = center_alignment
        
        headers = ["FECHA", "MOTIVO DE DETENCION", "ESTACION", "HORA DE DETENCION", "HORA INICIO OPERACION",
                "DURACION (seg)", "CABINA 1", "CABINA 2", "EVENTO", "TURNO", "OBSERVACIONES", "INPUTABLE", "OPERADOR"]
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment
        
        cont = 4

        # Itera sobre el queryset filtrado
        for stop in stop_reg:
            ws.cell(row= cont, column= 1).value = str(stop.registration_date)
            ws.cell(row= cont, column= 2).value = str(stop.stop_code)
            ws.cell(row= cont, column= 3).value = str(stop.station)
            ws.cell(row= cont, column= 4).value = str(stop.start_date)
            ws.cell(row= cont, column= 5).value = str(stop.end_date)
            ws.cell(row= cont, column= 6).value = str(stop.stop_time)
            ws.cell(row= cont, column= 7).value = str(stop.cabin)
            ws.cell(row= cont, column= 8).value = str(stop.cabin2)
            ws.cell(row= cont, column= 9).value = str(stop.event_type)
            ws.cell(row= cont, column= 10).value = str(stop.shift)
            ws.cell(row= cont, column= 11).value = str(stop.observation)
            ws.cell(row= cont, column= 12).value = str(stop.inputable)
            ws.cell(row= cont, column= 13).value = str(stop.operator)
            
            
            cont +=1
        
        # Ajustar el ancho de las columnas
        for col_num in range(1, len(headers) + 1):
            max_length = 0
            column_letter = ws.cell(row=3, column=col_num).column_letter
            for cell in ws[column_letter]:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
                    

        file_name = "Reporte_paradas_registradas.xlsx"
        response = HttpResponse(content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        content = "attachment; filename = {0}".format(file_name)
        response["Content-Disposition"] = content
        wb.save(response)
        return response
    


class ReporterExcelOperatorDay(TemplateView):
    def __init__(self, queryset = None):
        # Utiliza el queryset pasado en el constructor o todos los registros si no se pasa
        self.queryset = queryset or OperationTime.objects.all()
    
    def get(self, request, *args, **kwargs):
        # Aqui utilizamos el queryset filtrado en lugar de obtener todos los registros
        ope_reg = self.queryset        
        
        # Crea el archivo excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Jornada de operacion"
        
        # Estilos
        title_font = Font(bold=True, size=14)
        header_font = Font(bold=True)
        header_fill = PatternFill(start_color="13678A", end_color="13678A", fill_type="solid")
        center_alignment = Alignment(horizontal="center")
        
        ws["A1"] = "REPORTE JORNADA OPERACIONES"
        ws.merge_cells("A1:G1")
        ws["A1"].font = title_font
        ws["A1"].alignment = center_alignment
        
        headers = ["FECHA", "HORA INICIO", "HOROMETRO INICIO", "HORA FIN", "HOROMETRO FIN", "TIEMPO TOTAL", "OPERADOR"]
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_alignment
        
        cont = 4

        # Itera sobre el queryset filtrado
        for ope in ope_reg:
            ws.cell(row= cont, column= 1).value = str(ope.date)
            ws.cell(row= cont, column= 2).value = str(ope.start_time)
            ws.cell(row= cont, column= 3).value = str(ope.horometer_start)
            ws.cell(row= cont, column= 4).value = str(ope.end_time)
            ws.cell(row= cont, column= 5).value = str(ope.horometer_end)
            ws.cell(row= cont, column= 6).value = str(ope.total_time)
            ws.cell(row= cont, column= 7).value = str(ope.operator)
            
            cont +=1
        
        # Ajustar el ancho de las columnas
        for col_num in range(1, len(headers) + 1):
            max_length = 0
            column_letter = ws.cell(row=3, column=col_num).column_letter
            for cell in ws[column_letter]:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column_letter].width = adjusted_width
                    

        file_name = "Reporte_jornada_operacion.xlsx"
        response = HttpResponse(content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        content = "attachment; filename = {0}".format(file_name)
        response["Content-Disposition"] = content
        wb.save(response)
        return response