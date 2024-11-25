import base64
from PIL import Image
from io import BytesIO

# Cargar una imagen en binario y convertirla a base64
with Image.open("img1.jpg") as img:
    # Redimensionar la imagen
    img = img.resize((100, 100))

    # Crear un buffer de memoria para la imagen
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    # Convertir la imagen en memoria a base64
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        
    # Imprimir la imagen en base64
    print(img_base64)