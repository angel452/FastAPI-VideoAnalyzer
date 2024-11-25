#!/bin/bash

# Definir códigos de color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'  # Para resetear el color

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

# Iniciar Redis
print_info "Iniciando Redis..."
redis-server --daemonize yes

# Verificar que Redis está en ejecución
print_info "Verificando que Redis está en ejecución..."
sleep 2  # Esperar unos segundos para asegurar que Redis se haya iniciado

# Intentar conectarse a Redis
if redis-cli ping | grep -q "PONG"; then
  print_success "Redis está funcionando correctamente."
else
  print_error "Error: No se puede conectar a Redis."
  exit 1
fi

# Iniciar el servidor FastAPI (uvicorn)
print_info "Iniciando FastAPI..."
uvicorn main:app --reload --host 0.0.0.0 --port 8080 &

# Iniciar el worker de Celery
print_info "Iniciando worker de Celery..."
celery -A app.tasks.celery_app worker --loglevel=info
