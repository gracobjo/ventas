"""
🗄️ Configuración de Base de Datos
Utilidades para manejo de base de datos SQLite
"""

import sqlite3
import os
from typing import Optional
from pyspark.sql import SparkSession

# Configuración de base de datos
DATABASE_URL = "sqlite:///app/data/ecommerce.db"
DATABASE_PATH = "app/data/ecommerce.db"

def get_spark_session() -> SparkSession:
    """Obtiene una sesión de Spark configurada"""
    return SparkSession.builder \
        .appName("E-Commerce Analytics") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .getOrCreate()

async def init_database():
    """Inicializa la base de datos SQLite"""
    try:
        # Crear directorio de datos si no existe
        os.makedirs("app/data", exist_ok=True)
        
        # Conectar a SQLite
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Crear tablas si no existen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                model_type TEXT NOT NULL,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                training_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                response_time REAL,
                status_code INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar métricas iniciales del sistema
        cursor.execute('''
            INSERT OR IGNORE INTO system_metrics (metric_name, metric_value, metric_description)
            VALUES 
                ('total_products', 0, 'Número total de productos'),
                ('total_customers', 0, 'Número total de clientes'),
                ('total_sales', 0, 'Ventas totales'),
                ('system_version', 1.0, 'Versión del sistema')
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")

def get_database_connection():
    """Obtiene una conexión a la base de datos"""
    return sqlite3.connect(DATABASE_PATH)

def save_system_metric(metric_name: str, metric_value: float, description: str = ""):
    """Guarda una métrica del sistema"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics (metric_name, metric_value, metric_description)
            VALUES (?, ?, ?)
        ''', (metric_name, metric_value, description))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error guardando métrica: {e}")

def save_model_performance(model_name: str, model_type: str, accuracy: float = None, 
                          precision: float = None, recall: float = None, f1_score: float = None):
    """Guarda el rendimiento de un modelo"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO model_performance (model_name, model_type, accuracy, precision, recall, f1_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (model_name, model_type, accuracy, precision, recall, f1_score))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error guardando rendimiento del modelo: {e}")

def log_api_request(endpoint: str, method: str, response_time: float, status_code: int):
    """Registra una petición a la API"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_requests (endpoint, method, response_time, status_code)
            VALUES (?, ?, ?, ?)
        ''', (endpoint, method, response_time, status_code))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error registrando petición API: {e}")

def get_system_stats():
    """Obtiene estadísticas del sistema"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        # Obtener métricas más recientes
        cursor.execute('''
            SELECT metric_name, metric_value, metric_description, timestamp
            FROM system_metrics
            ORDER BY timestamp DESC
        ''')
        
        metrics = cursor.fetchall()
        
        # Obtener rendimiento de modelos
        cursor.execute('''
            SELECT model_name, model_type, accuracy, precision, recall, f1_score, training_date
            FROM model_performance
            ORDER BY training_date DESC
            LIMIT 10
        ''')
        
        models = cursor.fetchall()
        
        # Obtener estadísticas de API
        cursor.execute('''
            SELECT 
                COUNT(*) as total_requests,
                AVG(response_time) as avg_response_time,
                COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_requests
            FROM api_requests
            WHERE timestamp >= datetime('now', '-24 hours')
        ''')
        
        api_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            "metrics": [
                {
                    "name": metric[0],
                    "value": metric[1],
                    "description": metric[2],
                    "timestamp": metric[3]
                }
                for metric in metrics
            ],
            "models": [
                {
                    "name": model[0],
                    "type": model[1],
                    "accuracy": model[2],
                    "precision": model[3],
                    "recall": model[4],
                    "f1_score": model[5],
                    "training_date": model[6]
                }
                for model in models
            ],
            "api_stats": {
                "total_requests_24h": api_stats[0] if api_stats else 0,
                "avg_response_time": round(api_stats[1], 3) if api_stats and api_stats[1] else 0,
                "error_requests_24h": api_stats[2] if api_stats else 0
            }
        }
        
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return None

def cleanup_old_data(days: int = 30):
    """Limpia datos antiguos de la base de datos"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        # Limpiar métricas antiguas
        cursor.execute('''
            DELETE FROM system_metrics
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days))
        
        # Limpiar peticiones API antiguas
        cursor.execute('''
            DELETE FROM api_requests
            WHERE timestamp < datetime('now', '-{} days')
        '''.format(days))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Datos antiguos limpiados (más de {days} días)")
        
    except Exception as e:
        print(f"Error limpiando datos: {e}")

