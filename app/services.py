from app.tasks import process_frame
from celery.result import AsyncResult
from app.models import FrameData

def start_frame_processing(frame : FrameData):
    """
    Iniciar la tarea Celery para procesar el frame
    """
    frame_data = {
        "video_name": frame.video_name,
        "timestamp": frame.timestamp,
        "image": frame.image,
        "additional_info": frame.aditional_info,
    }
    
    """Inicia la tarea Celery para procesar el frame"""
    task = process_frame.apply_async(args=[frame_data]) # celerity 
    return task.id  

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
