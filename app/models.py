# app/models.py
from pydantic import BaseModel
from typing import List
from typing import Optional

# class Project(BaseModel):
#     project_name: str
#     description: str
#     url: str
#     login_page: str


class Project(BaseModel):
    project_name: str
    description: str
    url: str
    login_page: str
    user_login: str
    user_password: str
    sqli: bool
    csrf: bool 
    dos: bool   
    phishing: bool
    brute_force: bool




# Modelo de datos para la imagen que llega a la API
class FrameData(BaseModel):
    video_name : str                            # Nombre del video
    timestamp : float                           # Tiempo exacto del frame (segundos)
    image : str                                 # Imagen en base64
    aditional_info: Optional[str] = None        # Información adicional
    
# Modelo de datos para los objetos detectados por la IA
class DetectedObjects(BaseModel):
    video_name : str                            # Nombre del video
    timestamp : float                           # Tiempo exacto del frame (segundos)
    objects : List[str]                         # Lista de objetos detectados
    aditional_info: Optional[str] = None        # Información adicional