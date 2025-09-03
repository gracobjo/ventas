"""
🚀 Sistema de Análisis E-Commerce con IA
Backend principal con FastAPI + PySpark
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.api import summary, products, customers, forecast, recommendations
from app.utils.data_generator import DataGenerator
from app.utils.database import init_database

# Configuración de la aplicación
app = FastAPI(
    title="E-Commerce AI Analytics API",
    description="Sistema completo de análisis de datos e-commerce con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(summary.router, prefix="/api/v1", tags=["summary"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(customers.router, prefix="/api/v1", tags=["customers"])
app.include_router(forecast.router, prefix="/api/v1", tags=["forecast"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("🚀 Iniciando Sistema E-Commerce AI...")
    
    # Inicializar base de datos
    await init_database()
    
    # Generar datos sintéticos si no existen
    data_generator = DataGenerator()
    if not os.path.exists("app/data/products.parquet"):
        print("📊 Generando datos sintéticos...")
        data_generator.generate_all_data()
        print("✅ Datos sintéticos generados")
    
    print("✅ Sistema iniciado correctamente")

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "🚀 E-Commerce AI Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": request.url.path
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

