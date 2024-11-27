import random
import datetime
import psycopg2

db_host = "localhost"
db_name = "operacion_cable"
db_user = "odt_admin"
db_password = "SopODT2024*"

try:
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

# cont = 1

# while cont <= 163:
#     registro = {"code": cont}
#     cont = cont + 1
    


#     cursor.execute(f"""
#     INSERT INTO registro_paradas_cabin2 (code) VALUES ('{registro['code']}')               
#     """)


cont = 2

while cont <= 56:
    registro = {
        "object_id": cont,
        "content_type_id": 15,
        "event_type_id": 2
        }
    cont = cont + 1
    


    cursor.execute(f"""
    INSERT INTO registro_paradas_eventstopcode (object_id, content_type_id, event_type_id) 
    VALUES ('{registro['object_id']}', '{registro['content_type_id']}', '{registro['event_type_id']}')               
    """)


conn.commit()

conn.close()