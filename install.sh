#!/bin/bash
# Script de instalación y configuración del proyecto
# Sistema de Gestión de Prácticas Profesionales

set -e  # Salir si hay errores

echo "======================================================"
echo "Sistema de Gestión de Prácticas Profesionales"
echo "Instalación y Configuración"
echo "======================================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_step() {
    echo -e "${GREEN}[PASO]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar Python
print_step "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_info "Versión de Python: $PYTHON_VERSION"

# Verificar PostgreSQL
print_step "Verificando PostgreSQL..."
if ! command -v psql &> /dev/null; then
    print_error "PostgreSQL no está instalado"
    print_info "Instala PostgreSQL: brew install postgresql (macOS)"
    exit 1
fi
print_info "PostgreSQL está instalado"

# Verificar Redis
print_step "Verificando Redis..."
if ! command -v redis-server &> /dev/null; then
    print_error "Redis no está instalado"
    print_info "Instala Redis: brew install redis (macOS)"
    exit 1
fi
print_info "Redis está instalado"

# Crear entorno virtual
print_step "Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_info "Entorno virtual creado"
else
    print_info "Entorno virtual ya existe"
fi

# Activar entorno virtual
print_step "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
print_step "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
print_step "Instalando dependencias..."
pip install -r requirements.txt
print_info "Dependencias instaladas"

# Copiar archivo .env
print_step "Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_info "Archivo .env creado. Por favor, edita .env con tus configuraciones."
else
    print_info "Archivo .env ya existe"
fi

# Crear directorios necesarios
print_step "Creando directorios..."
mkdir -p logs
mkdir -p media
mkdir -p static
mkdir -p staticfiles
print_info "Directorios creados"

# Generar apps faltantes
print_step "Generando estructura de aplicaciones..."
if [ -f "generate_apps.py" ]; then
    python generate_apps.py
    print_info "Apps generadas"
fi

# Crear base de datos
print_step "Configurando base de datos PostgreSQL..."
print_info "Asegúrate de que PostgreSQL esté ejecutándose"

# Intentar crear la base de datos
DB_NAME="practicas_db"
DB_USER="postgres"

print_info "Creando base de datos $DB_NAME..."
createdb $DB_NAME 2>/dev/null || print_info "La base de datos ya existe o necesitas crearla manualmente"

# Aplicar migraciones
print_step "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate
print_info "Migraciones aplicadas"

# Recopilar archivos estáticos
print_step "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput
print_info "Archivos estáticos recopilados"

# Crear superusuario
print_step "¿Deseas crear un superusuario? (s/n)"
read -r response
if [[ "$response" =~ ^([sS])$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "======================================================"
echo -e "${GREEN}Instalación completada exitosamente!${NC}"
echo "======================================================"
echo ""
echo "Para iniciar el proyecto:"
echo ""
echo "1. Activar entorno virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. Iniciar Redis (en una terminal separada):"
echo "   redis-server"
echo ""
echo "3. Iniciar Celery Worker (en una terminal separada):"
echo "   celery -A config worker -l info"
echo ""
echo "4. Iniciar Celery Beat (en una terminal separada):"
echo "   celery -A config beat -l info"
echo ""
echo "5. Iniciar servidor Django:"
echo "   python manage.py runserver"
echo ""
echo "6. Acceder a:"
echo "   - API: http://localhost:8000/api/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
echo "O usar Docker:"
echo "   docker-compose up --build"
echo ""
echo "======================================================"
