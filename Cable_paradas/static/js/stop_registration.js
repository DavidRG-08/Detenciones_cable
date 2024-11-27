$(document).ready(function() {
    $('.select2').select2({
        placeholder: "Selecciona un código de parada",
        allowClear: true
    });


    // Escuchar el cambio en el campo event_type
    $('#id_event_type').change(function(){
        var eventTypeId = $(this).val();  // Obtener el valor seleccionado
        var url = $('#load-stop-codes-url').val();  // Obtener la URL del campo oculto

        if (eventTypeId) {
            $.ajax({
                url: url,  // URL para cargar códigos de parada
                data: {
                    'event_type_id': eventTypeId  // Enviar el ID del tipo de evento
                },
                success: function(data) {
                    // Limpiar las opciones actuales del select de stopCode
                    $("#id_stop_code").empty();
                    // Agregar las nuevas opciones obtenidas desde el servidor
                    $.each(data, function(index, value) {
                        $("#id_stop_code").append('<option value="' + value.id + '">' + value.name + '</option>');
                    });
                }
            });
        } else {
            // Si no hay evento seleccionado, limpiar el campo stopCode
            $("#id_stop_code").empty();
            $("#id_stop_code_value").append('<option value="">Seleccione un código de parada</option>');
        }
    });


    // Función para calcular la diferencia entre dos horas
    function calculateDuration() {
        var startTime = $('#id_start_date').val();
        var endTime = $('#id_end_date').val();

        if (startTime && endTime) {
            var start = new Date("1970-01-01T" + startTime + "Z");
            var end = new Date("1970-01-01T" + endTime + "Z");

            // Si el tiempo de finalización es menor que el de inicio, sumamos un día
            if (end < start) {
                end.setDate(end.getDate() + 1);
            }

            // Calcula la diferencia en milisegundos y luego en segundos
            var duration = (end - start) / 1000;
            
            // Mostrar la duración en el campo de duración
            $('#id_stop_time').val(duration);
        }
    }

    // Escuchar los cambios en los campos start_date y end_date
    $('#id_start_date, #id_end_date').change(function(){
        calculateDuration();
    });

});

