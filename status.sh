#!/bin/bash

# Definir códigos de color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'  # Para resetear el color

# URL de la API por defecto
DEFAULT_URL="http://127.0.0.1:8080"

# Función para imprimir mensajes con colores
print_info() {
    echo -e "${BLUE}$1${RESET}"
}

print_success() {
    echo -e "${GREEN}$1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}$1${RESET}"
}

print_error() {
    echo -e "${RED}$1${RESET}"
}

# Usar la URL por defecto
URL=$DEFAULT_URL

# Preguntar por los datos de la imagen
print_info "Por favor ingresa el nombre del video:"
read video_name

print_info "Por favor ingresa el timestamp:"
read timestamp

print_info "Por favor ingresa el nombre de la imagen (base64):"
read image_base64

print_info "Por favor ingresa información adicional sobre el video:"
read aditional_info


# Crear el JSON con los datos proporcionados
JSON_DATA=$(cat <<EOF
{
  "video_name": "$video_name",
  "timestamp": "$timestamp",
  "image": "$image_base64",
  "aditional_info": "$aditional_info"
}
EOF
)

# Crear el JSON con los datos proporcionados
#JSON_DATA=$(cat <<EOF
#{
#  "project_name": "probe name",
#  "description": "esto es una descripcion",
#  "url": "http://google.com",
#  "login_page": "http://google.com/admin"
#}
#EOF
#)

#JSON_DATA=$(cat <<EOF
#{
#  "project_name": "probe name",
#  "description": "Descripción del proyecto",
#  "url": "http://google.com",
#  "login_page": "http://google.com/admin",
#  "user_login": "admin",
#  "user_password": "password",
#  "sqli": "false",
#  "csrf": "true",
#  "dos": "true",
#  "phishing": "true",
#  "brute_force": "true"
#}
#EOF
#)
    
# Enviar la solicitud POST
response=$(curl -X POST "$URL/receive_frame" -H "Content-Type: application/json" -d "$JSON_DATA")

# Extraer el frame_id del JSON de respuesta
task_id=$(echo $response | jq -r '.task_id')

if [ "$task_id" == "null" ]; then
  print_error "Error al obtener el task_id."
  exit 1
fi

print_success "Fame recibido con task_id: $task_id"

# Preguntar si desea verificar el estado
while true; do
  print_info "¿Quieres consultar el estado de la tarea? (s/n)"
  read user_input
  
  if [[ "$user_input" == "s" || "$user_input" == "S" ]]; then
    # Consultar el estado de la tarea
    status_response=$(curl -X POST -s "$URL/task_status/$task_id")
    status=$(echo $status_response | jq -r '.status')
    
    # Mostrar el estado de la tarea
    echo -e "${CYAN}Estado de la tarea: $status${RESET}"

    # Si la tarea ha terminado, mostrar el resultado o error
    if [ "$status" == "Completado" ] || [ "$status" == "Fallido" ]; then
      result=$(echo $status_response | jq -r '.result')
      error=$(echo $status_response | jq -r '.error')
      
      if [ "$status" == "Completado" ]; then
        print_success "Resultado: $result"
      else
        print_error "Error: $error"
      fi
      break
    fi
    
    # Esperar 5 segundos antes de hacer otra consulta
    sleep 5
  elif [[ "$user_input" == "n" || "$user_input" == "N" ]]; then
    print_warning "Consultas de estado desactivadas. Saliendo."
    break
  else
    print_error "Entrada no válida. Por favor ingresa 's' o 'n'."
  fi
done
