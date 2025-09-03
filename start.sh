#!/bin/bash

# 🚀 Script de inicio para Sistema E-Commerce AI Analytics
# Este script facilita el inicio rápido del proyecto

echo "🚀 Iniciando Sistema E-Commerce AI Analytics..."
echo "================================================"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

echo "✅ Docker y Docker Compose están disponibles"

# Función para mostrar el menú
show_menu() {
    echo ""
    echo "📋 Opciones disponibles:"
    echo "1) 🐳 Iniciar con Docker Compose (recomendado)"
    echo "2) 🔧 Iniciar solo Backend (desarrollo)"
    echo "3) ⚛️  Iniciar solo Frontend (desarrollo)"
    echo "4) 🧪 Ejecutar tests"
    echo "5) 📊 Generar datos sintéticos"
    echo "6) 🛑 Detener todos los servicios"
    echo "7) 📖 Ver documentación"
    echo "8) 🚪 Salir"
    echo ""
    read -p "Selecciona una opción (1-8): " choice
}

# Función para iniciar con Docker Compose
start_docker() {
    echo "🐳 Iniciando servicios con Docker Compose..."
    docker-compose up -d
    
    echo ""
    echo "✅ Servicios iniciados correctamente!"
    echo "📊 Backend API: http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
    echo "⚛️  Frontend: http://localhost:3000"
    echo ""
    echo "🔄 Para ver logs: docker-compose logs -f"
    echo "🛑 Para detener: docker-compose down"
}

# Función para iniciar solo Backend
start_backend() {
    echo "🔧 Iniciando solo Backend..."
    cd backend
    
    # Verificar si existe un entorno virtual
    if [ ! -d "venv" ]; then
        echo "📦 Creando entorno virtual..."
        python -m venv venv
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Instalar dependencias
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    
    # Iniciar servidor
    echo "🚀 Iniciando servidor FastAPI..."
    python main.py &
    
    cd ..
    echo ""
    echo "✅ Backend iniciado en http://localhost:8000"
    echo "📖 API Docs: http://localhost:8000/docs"
}

# Función para iniciar solo Frontend
start_frontend() {
    echo "⚛️  Iniciando solo Frontend..."
    cd frontend
    
    # Verificar si node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "📦 Instalando dependencias..."
        npm install
    fi
    
    # Iniciar servidor de desarrollo
    echo "🚀 Iniciando servidor de desarrollo..."
    npm start &
    
    cd ..
    echo ""
    echo "✅ Frontend iniciado en http://localhost:3000"
}

# Función para ejecutar tests
run_tests() {
    echo "🧪 Ejecutando tests..."
    cd backend
    
    # Activar entorno virtual si existe
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Instalar pytest si no está instalado
    pip install pytest pytest-asyncio
    
    # Ejecutar tests
    python -m pytest ../tests/ -v
    
    cd ..
}

# Función para generar datos sintéticos
generate_data() {
    echo "📊 Generando datos sintéticos..."
    cd backend
    
    # Activar entorno virtual si existe
    if [ -d "venv" ]; then
        source venv/bin/activate
    fi
    
    # Ejecutar script de generación de datos
    python -c "
import sys
sys.path.append('app')
from utils.data_generator import DataGenerator

print('Generando datos sintéticos...')
generator = DataGenerator()
generator.generate_all_data()
print('✅ Datos sintéticos generados correctamente')
"
    
    cd ..
}

# Función para detener servicios
stop_services() {
    echo "🛑 Deteniendo servicios..."
    docker-compose down
    echo "✅ Servicios detenidos"
}

# Función para mostrar documentación
show_docs() {
    echo "📖 Documentación del proyecto:"
    echo "=============================="
    echo ""
    echo "📚 README.md - Documentación principal"
    echo "🔗 API Docs: http://localhost:8000/docs (cuando el backend esté corriendo)"
    echo "🔗 ReDoc: http://localhost:8000/redoc (cuando el backend esté corriendo)"
    echo ""
    echo "📁 Estructura del proyecto:"
    echo "  backend/     - API FastAPI + PySpark + ML"
    echo "  frontend/    - React + Tailwind + Framer Motion"
    echo "  data/        - Datos sintéticos"
    echo "  tests/       - Tests unitarios"
    echo ""
    echo "🚀 Endpoints principales:"
    echo "  GET /api/v1/summary           - Resumen general"
    echo "  GET /api/v1/products/top      - Top productos"
    echo "  GET /api/v1/customers/rfm     - Análisis RFM"
    echo "  GET /api/v1/forecast          - Pronósticos"
    echo "  GET /api/v1/recommendations/{id} - Recomendaciones"
}

# Bucle principal
while true; do
    show_menu
    
    case $choice in
        1)
            start_docker
            ;;
        2)
            start_backend
            ;;
        3)
            start_frontend
            ;;
        4)
            run_tests
            ;;
        5)
            generate_data
            ;;
        6)
            stop_services
            ;;
        7)
            show_docs
            ;;
        8)
            echo "👋 ¡Hasta luego!"
            exit 0
            ;;
        *)
            echo "❌ Opción inválida. Por favor selecciona 1-8."
            ;;
    esac
    
    echo ""
    read -p "Presiona Enter para continuar..."
done

