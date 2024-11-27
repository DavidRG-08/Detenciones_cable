import random
import datetime
import psycopg2

# ... (Definición de parámetros de conexión y funciones para generar registros)
# Parámetros de conexión a la base de datos PostgreSQL
db_host = "localhost"  # Cambiar por la dirección del servidor de base de datos
db_name = "operacion_cable"  # Cambiar por el nombre de tu base de datos
db_user = "david"  # Cambiar por el nombre de usuario de la base de datos
db_password = "A12345"  # Cambiar por la contraseña de la base de datos

try:
    # Establecer conexión con la base de datos
    conexion = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = conexion.cursor()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

# Rango de fechas
fecha_inicio = datetime.date(2024, 1, 1)
fecha_fin = datetime.date(2024, 6, 30)

for _ in range(2327):
    # Generar registro aleatorio
    registro = {
        "registration_date": f"2024-{random.randint(1, 12)}-{random.randint(1, 28)}",
        "start_date": random.choice([fecha_inicio + datetime.timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days + 1)]).strftime("%Y-%m-%d"),
        "end_date": random.choice([fecha_inicio + datetime.timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days + 1)]).strftime("%Y-%m-%d"),
        "stop_time": random.randint(1, 5),
        "observation": "Observaciones",
        "inputable": "True",
        "cabin2_id": random.randint(1, 163),
        "cabin_id": random.randint(1, 163),
        "operator_id": random.randint(1, 4),
        "shift_id": random.randint(1, 2),
        "station_id": random.randint(1, 5),
        "stopCode_id": random.choice(["C-0011", "A-0014", "B-0026", "D-0014", "A-0001", "A-0007", "A-0012", "A-0013", "A-0015", "A-0016", "A-0019", "B-0007", "B-0008", "B-0009", "B-0012", "B-0023", "B-0025", "C-0014", "C-0017", "C-0018", "C-0025", "C-0028", "C-0098", "D-0002", "D-0005", "D-0009", "D- 0011", "D-0066"]),
        "event_type_id": random.randint(1, 3)
    }

# print(f"INSERT INTO registro_paradas_stopregistration (registration_date, start_date, end_date, stop_time, observation, inputable, cabin2_id, cabin_id, operator_id, shift_id, station_id, stopCode_id) VALUES ('{registro['registration_date']}', '{registro['start_date']}', '{registro['end_date']}', {registro['stop_time']}, '{registro['observation']}', '{registro['inputable']}', {registro['cabin2_id']}, {registro['cabin_id']}, {registro['operator_id']}, {registro['shift_id']}, {registro['station_id']}, '{registro['stopCode_id']}');")

    # Insertar registro en la tabla
    cursor.execute(f"""
    INSERT INTO registro_paradas_stopregistration (registration_date, start_date, end_date, stop_time, observation, inputable, cabin2_id, cabin_id, operator_id, shift_id, station_id, "stopCode_id", event_type_id) 
    VALUES ('{registro['registration_date']}', '{registro['start_date']}', '{registro['end_date']}', {registro['stop_time']}, '{registro['observation']}', '{registro['inputable']}', {registro['cabin2_id']}, {registro['cabin_id']}, {registro['operator_id']}, {registro['shift_id']}, {registro['station_id']}, '{registro['stopCode_id']}', {registro['event_type_id']});
    """)

# Guardar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión
conexion.close()
