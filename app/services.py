from app.tasks import process_frame
from celery.result import AsyncResult
from app.models import FrameData, ObjectDetection
from pyhive import hive
import sys
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_hive(host, port, username, database):
    try:
        # Establecer la conexión
        conn = hive.Connection(host=host, port=port, username=username, database=database)
        logger.info("Conexión exitosa a Hive.")
        return conn
    except Exception as e:
        logger.error(f"Error al conectar con Hive: {e}")
        sys.exit(1)

def execute_query(cursor, query):
    try:
        # Ejecutar la consulta
        cursor.execute(query)
        # Obtener los resultados
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        logger.error(f"Error al ejecutar la consulta: {e}")
        return []


def start_frame_processing(frame : ObjectDetection):
    """
    Iniciar la tarea Celery para procesar el frame
    
    frame_data = {
        "video_name": frame.video_name,
        "objects_detected": frame.objects,
    }
    """

    """Inicia la tarea Celery para procesar el frame
    task = process_frame.apply_async(args=[frame_data]) # celerity 
    return task.id  
    """
    try:
        """
        Iniciar la consulta a Hive para procesar el frame
        """
    
        # Parámetros de conexión (ajusta estos valores según tu entorno)
        host = "localhost"  # Cambia con la URL de tu clúster EMR
        port = 10000  # Puerto predeterminado de Hive
        username = "hive"  # Usuario Hive
        database = "default"  # Base de datos Hive (ajusta según tu configuración)

        # Conectar a Hive
        conn = connect_to_hive(host, port, username, database)
        cursor = conn.cursor()

        # Ejecutar la consulta en Hive. Aquí se usa la consulta desde el frame que se recibe
        #query = f"SELECT * FROM {frame.video_name} LIMIT 10"  # Modificar según sea necesario
        # Consulta en Hive que relaciona objetos, escenarios y características
        query = f"""
        SELECT 
            o.object_name, 
            o.x1, 
            o.y1, 
            o.x2, 
            o.y2, 
            o.rgb_color, 
            o.proximity, 
            o.sec AS object_sec, 
            s.environment_type, 
            s.description AS scenario_description, 
            s.weather, 
            s.time_of_day, 
            s.terrain, 
            s.crowd_level, 
            s.lighting, 
            f.description AS feature_description, 
            f.color1, 
            f.color2, 
            f.size, 
            f.orientation, 
            f.type
        FROM 
            objects o
        JOIN 
            scenarios s ON o.video_name = s.video_name
        JOIN 
            features f ON o.video_name = f.video_name AND o.object_name = f.object_name
        WHERE 
            o.object_name = '{frame.objects}' 
            AND o.video_name = '{frame.video_name}'
        LIMIT 10;
        """

        logger.info(f"Ejecutando consulta: {query}")

        # Obtener los resultados de la consulta
        resultados = execute_query(cursor, query)

        if resultados:
            logger.info("Resultados de la consulta:")
            for fila in resultados:
                logger.info(fila)
        else:
            logger.info("No se encontraron resultados.")

        # Cerrar la conexión a Hive
        cursor.close()
        conn.close()

        # Formatear el resultado en JSON
        response_data = []
        for row in resultados:
            response_data.append({
                "object_name": row[0],
                "coordinates": {  # Corregir los dos puntos extra
                    "x1": row[1],
                    "y1": row[2],
                    "x2": row[3],
                    "y2": row[4],
                },
                "rgb_color": row[5],
                "proximity": row[6],
                "object_sec": row[7],
                "scenario": {  # Corregir los dos puntos extra
                    "environment_type": row[8],
                    "scenario_description": row[9],  # Corregir el nombre de la clave
                    "weather": row[10],
                    "time_of_day": row[11],
                    "terrain": row[12],
                    "crowd_level": row[13],
                    "lighting": row[14],
                },
                "feature": {  # Corregir los dos puntos extra
                    "feature_description": row[15],  # Corregir el nombre de la clave
                    "color1": row[16],
                    "color2": row[17],
                    "size": row[18],
                    "orientation": row[19],
                    "type": row[20],
                }
            })

        return {"message": "Consulta ejecutada correctamente", "results": response_data}
    
    except Exception as e:
        logger.error(f"Error al procesar el frame: {e}")
        return {"message": "Error en el procesamiento", "error": str(e)}

def get_frame_task_status(task_id: str):
    """
    Consulta el estado de la tarea de un frame
    """

    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        return {"status": "En proceso"}
    elif task.state == 'SUCCESS':
        return {"status": "Completado", "result": task.result}
    elif task.state == 'FAILURE':
        return {"status": "Fallido", "error": str(task.result)}
    return {"status": "Estado desconocido"}
    