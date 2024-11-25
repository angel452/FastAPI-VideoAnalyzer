from fastapi import APIRouter
from app.models import FrameData
from app.services import start_frame_processing, get_frame_task_status
from app.logger_config import setup_logger 

# Configurar el logger con el nombre del archivo actual
logger = setup_logger(__name__)

router = APIRouter()

# Ruta para recibir un frame de video y empezar su procesamiento
@router.post("/receive_frame")
async def receive_frame(frame: FrameData):
    """Recibe el video y comienza el procesamiento en segundo plano para generar un indice invertido"""
    
    logger.info(f"Recibiendo video: {frame.video_name} - timestamp: {frame.timestamp}")
    logger.info(f"Datos completos del video: {frame.dict()}")
    task_id = start_frame_processing(frame)
    
    logger.info(f"Tarea iniciada con task_id: {task_id}")
    
    return {"message": "El procesamiento del frame está en marcha", "task_id": task_id}

# Ruta para consultar el estado de la tarea de procesamiento de un frame
@router.post("/task_status/{task_id}")
async def frame_status(task_id: str):
    """
    Consulta el estado de la tarea de procesamiento de un frame.
    """
    
    logger.info(f"Consultando el estado de la tarea con ID: {task_id}")
    
    status = get_frame_task_status(task_id)
    
    if status["status"] == "Error":
        logger.error(f"Tarea {task_id} no encontrada")
    else:
        logger.info(f"Estado de la tarea {task_id}: {status['status']}")
    
    return status