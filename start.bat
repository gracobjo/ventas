@echo off
chcp 65001 >nul

REM 🚀 Script de inicio para Sistema E-Commerce AI Analytics (Windows)
REM Este script facilita el inicio rápido del proyecto en Windows

echo 🚀 Iniciando Sistema E-Commerce AI Analytics...
echo ================================================

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado. Por favor instala Docker Desktop primero.
    pause
    exit /b 1
)

REM Verificar si Docker Compose está instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose no está instalado. Por favor instala Docker Compose primero.
    pause
    exit /b 1
)

echo ✅ Docker y Docker Compose están disponibles

:menu
echo.
echo 📋 Opciones disponibles:
echo 1) 🐳 Iniciar con Docker Compose (recomendado)
echo 2) 🔧 Iniciar solo Backend (desarrollo)
echo 3) ⚛️  Iniciar solo Frontend (desarrollo)
echo 4) 🧪 Ejecutar tests
echo 5) 📊 Generar datos sintéticos
echo 6) 🛑 Detener todos los servicios
echo 7) 📖 Ver documentación
echo 8) 🚪 Salir
echo.
set /p choice="Selecciona una opción (1-8): "

if "%choice%"=="1" goto start_docker
if "%choice%"=="2" goto start_backend
if "%choice%"=="3" goto start_frontend
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto generate_data
if "%choice%"=="6" goto stop_services
if "%choice%"=="7" goto show_docs
if "%choice%"=="8" goto exit
echo ❌ Opción inválida. Por favor selecciona 1-8.
pause
goto menu

:start_docker
echo 🐳 Iniciando servicios con Docker Compose...
docker-compose up -d
echo.
echo ✅ Servicios iniciados correctamente!
echo 📊 Backend API: http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
echo ⚛️  Frontend: http://localhost:3000
echo.
echo 🔄 Para ver logs: docker-compose logs -f
echo 🛑 Para detener: docker-compose down
pause
goto menu

:start_backend
echo 🔧 Iniciando solo Backend...
cd backend

REM Verificar si existe un entorno virtual
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt

REM Iniciar servidor
echo 🚀 Iniciando servidor FastAPI...
start python main.py

cd ..
echo.
echo ✅ Backend iniciado en http://localhost:8000
echo 📖 API Docs: http://localhost:8000/docs
pause
goto menu

:start_frontend
echo ⚛️  Iniciando solo Frontend...
cd frontend

REM Verificar si node_modules existe
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    npm install
)

REM Iniciar servidor de desarrollo
echo 🚀 Iniciando servidor de desarrollo...
start npm start

cd ..
echo.
echo ✅ Frontend iniciado en http://localhost:3000
pause
goto menu

:run_tests
echo 🧪 Ejecutando tests...
cd backend

REM Activar entorno virtual si existe
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Instalar pytest si no está instalado
pip install pytest pytest-asyncio

REM Ejecutar tests
python -m pytest ..\tests\ -v

cd ..
pause
goto menu

:generate_data
echo 📊 Generando datos sintéticos...
cd backend

REM Activar entorno virtual si existe
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Ejecutar script de generación de datos
python -c "import sys; sys.path.append('app'); from utils.data_generator import DataGenerator; print('Generando datos sintéticos...'); generator = DataGenerator(); generator.generate_all_data(); print('✅ Datos sintéticos generados correctamente')"

cd ..
pause
goto menu

:stop_services
echo 🛑 Deteniendo servicios...
docker-compose down
echo ✅ Servicios detenidos
pause
goto menu

:show_docs
echo 📖 Documentación del proyecto:
echo ==============================
echo.
echo 📚 README.md - Documentación principal
echo 🔗 API Docs: http://localhost:8000/docs (cuando el backend esté corriendo)
echo 🔗 ReDoc: http://localhost:8000/redoc (cuando el backend esté corriendo)
echo.
echo 📁 Estructura del proyecto:
echo   backend/     - API FastAPI + PySpark + ML
echo   frontend/    - React + Tailwind + Framer Motion
echo   data/        - Datos sintéticos
echo   tests/       - Tests unitarios
echo.
echo 🚀 Endpoints principales:
echo   GET /api/v1/summary           - Resumen general
echo   GET /api/v1/products/top      - Top productos
echo   GET /api/v1/customers/rfm     - Análisis RFM
echo   GET /api/v1/forecast          - Pronósticos
echo   GET /api/v1/recommendations/{id} - Recomendaciones
pause
goto menu

:exit
echo 👋 ¡Hasta luego!
exit /b 0

