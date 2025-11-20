#!/bin/bash

# Script para ejecutar pruebas unitarias automatizadas
# con cobertura de código

set -e  # Salir si hay algún error

echo "🧪 Ejecutando pruebas unitarias automatizadas..."
echo "================================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo -e "${RED}❌ Error: No se encuentra manage.py${NC}"
    echo "Ejecuta este script desde la raíz del proyecto"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Verificar que pytest está instalado
if ! python -c "import pytest" &> /dev/null; then
    echo -e "${RED}❌ Error: pytest no está instalado${NC}"
    echo "Instala las dependencias con: pip install -r requirements.txt"
    exit 1
fi

# Limpiar archivos de caché
echo -e "${BLUE}🧹 Limpiando caché...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
rm -rf htmlcov/ .coverage 2>/dev/null || true
echo ""

# Función para ejecutar pruebas
run_tests() {
    local test_path=$1
    local description=$2
    
    echo -e "${BLUE}📝 $description${NC}"
    echo "─────────────────────────────────────────────"
    
    if pytest "$test_path" -v --tb=short; then
        echo -e "${GREEN}✅ $description - PASADAS${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}❌ $description - FALLIDAS${NC}"
        echo ""
        return 1
    fi
}

# Variable para contar errores
failed_tests=0

# Opciones de ejecución
case "${1:-all}" in
    all)
        echo -e "${YELLOW}🚀 Ejecutando TODAS las pruebas con cobertura...${NC}"
        echo ""
        
        if pytest --cov=apps --cov=config \
                  --cov-report=html \
                  --cov-report=term-missing:skip-covered \
                  --cov-config=.coveragerc \
                  -v --tb=short; then
            echo ""
            echo -e "${GREEN}✅ TODAS LAS PRUEBAS PASARON${NC}"
            echo ""
            echo -e "${BLUE}📊 Reporte de cobertura generado en: htmlcov/index.html${NC}"
            echo -e "${BLUE}   Abre el reporte con: open htmlcov/index.html${NC}"
        else
            echo ""
            echo -e "${RED}❌ ALGUNAS PRUEBAS FALLARON${NC}"
            exit 1
        fi
        ;;
    
    usuarios)
        run_tests "apps/usuarios/tests/" "Pruebas de Usuarios" || ((failed_tests++))
        ;;
    
    models)
        echo -e "${YELLOW}🧪 Ejecutando pruebas de MODELOS...${NC}"
        echo ""
        pytest -m models -v --tb=short || ((failed_tests++))
        ;;
    
    views)
        echo -e "${YELLOW}🧪 Ejecutando pruebas de VISTAS/API...${NC}"
        echo ""
        pytest -m views -v --tb=short || ((failed_tests++))
        ;;
    
    api)
        echo -e "${YELLOW}🧪 Ejecutando pruebas de API...${NC}"
        echo ""
        pytest -m api -v --tb=short || ((failed_tests++))
        ;;
    
    quick)
        echo -e "${YELLOW}⚡ Ejecutando pruebas RÁPIDAS (sin las lentas)...${NC}"
        echo ""
        pytest -m "not slow" -v --tb=short || ((failed_tests++))
        ;;
    
    coverage)
        echo -e "${YELLOW}📊 Generando reporte de cobertura...${NC}"
        echo ""
        pytest --cov=apps --cov=config \
               --cov-report=html \
               --cov-report=term \
               --cov-config=.coveragerc \
               -v --tb=short
        
        echo ""
        echo -e "${BLUE}📊 Reporte generado en: htmlcov/index.html${NC}"
        echo -e "${BLUE}   Abre con: open htmlcov/index.html${NC}"
        ;;
    
    watch)
        echo -e "${YELLOW}👀 Modo WATCH - Las pruebas se ejecutarán al detectar cambios${NC}"
        echo -e "${BLUE}   Presiona Ctrl+C para detener${NC}"
        echo ""
        
        # Requiere pytest-watch (instalable con: pip install pytest-watch)
        if python -c "import pytest_watch" &> /dev/null; then
            ptw -- -v --tb=short
        else
            echo -e "${RED}❌ pytest-watch no está instalado${NC}"
            echo "Instálalo con: pip install pytest-watch"
            exit 1
        fi
        ;;
    
    help|--help|-h)
        echo "Uso: ./run_tests.sh [opción]"
        echo ""
        echo "Opciones:"
        echo "  all         - Ejecutar todas las pruebas con cobertura (por defecto)"
        echo "  usuarios    - Ejecutar solo pruebas de usuarios"
        echo "  models      - Ejecutar solo pruebas de modelos"
        echo "  views       - Ejecutar solo pruebas de vistas/API"
        echo "  api         - Ejecutar solo pruebas de API"
        echo "  quick       - Ejecutar pruebas rápidas (excluye lentas)"
        echo "  coverage    - Generar reporte de cobertura detallado"
        echo "  watch       - Modo watch (ejecuta pruebas al detectar cambios)"
        echo "  help        - Mostrar esta ayuda"
        echo ""
        echo "Ejemplos:"
        echo "  ./run_tests.sh                  # Ejecutar todas las pruebas"
        echo "  ./run_tests.sh usuarios         # Solo pruebas de usuarios"
        echo "  ./run_tests.sh quick            # Pruebas rápidas"
        echo "  ./run_tests.sh coverage         # Con reporte de cobertura"
        echo ""
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ Opción no reconocida: $1${NC}"
        echo "Usa './run_tests.sh help' para ver las opciones disponibles"
        exit 1
        ;;
esac

# Resumen final
if [ $failed_tests -gt 0 ]; then
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}❌ $failed_tests grupo(s) de pruebas fallaron${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Todas las pruebas completadas exitosamente${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
fi
