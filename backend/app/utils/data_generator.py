"""
📊 Generador de datos sintéticos usando PySpark
Refactorizado del código original para usar Spark DataFrames
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import warnings

warnings.filterwarnings('ignore')
np.random.seed(42)

class DataGenerator:
    """Generador de datos sintéticos para e-commerce usando PySpark"""
    
    def __init__(self):
        # Inicializar Spark
        self.spark = SparkSession.builder \
            .appName("E-Commerce Data Generator") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        # Configurar logging
        self.spark.sparkContext.setLogLevel("WARN")
        
        self.productos = [
            'iPhone 15', 'Samsung Galaxy S24', 'MacBook Pro', 'Dell XPS',
            'Nike Air Force', 'Adidas Stan Smith', 'Levi\'s 501', 'Zara Jacket',
            'Sony WH-1000XM5', 'AirPods Pro', 'Canon EOS R5', 'GoPro Hero 12',
            'PlayStation 5', 'Xbox Series X', 'Nintendo Switch', 'Steam Deck'
        ]
        
        self.categorias = [
            'Smartphones', 'Laptops', 'Calzado', 'Ropa',
            'Audio', 'Cámaras', 'Gaming'
        ]
        
        self.ciudades = [
            'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao',
            'Málaga', 'Murcia', 'Palma', 'Las Palmas', 'Zaragoza'
        ]
    
    def generar_productos(self, n=100):
        """Genera catálogo de productos usando Spark"""
        print(f"📦 Generando {n} productos...")
        
        # Crear datos con pandas primero (más fácil para datos pequeños)
        productos_data = []
        
        for i in range(n):
            categoria = np.random.choice(self.categorias)
            
            # Precios realistas por categoría
            if categoria in ['Smartphones', 'Laptops']:
                precio_base = np.random.uniform(300, 1500)
            elif categoria in ['Audio', 'Cámaras']:
                precio_base = np.random.uniform(50, 800)
            elif categoria == 'Gaming':
                precio_base = np.random.uniform(200, 600)
            else:
                precio_base = np.random.uniform(20, 200)
            
            productos_data.append({
                'product_id': f'P{i:03d}',
                'nombre': str(np.random.choice(self.productos)) + f' {i}',
                'categoria': str(categoria),
                'precio': float(precio_base),
                'costo': float(precio_base * 0.6),  # 40% margen
                'stock': int(np.random.randint(0, 500)),
                'rating_promedio': float(np.random.uniform(3.0, 5.0)),
                'num_reviews': int(np.random.randint(0, 1000))
            })
        
        # Convertir a Spark DataFrame
        df_pandas = pd.DataFrame(productos_data)
        df_spark = self.spark.createDataFrame(df_pandas)
        
        return df_spark
    
    def generar_clientes(self, n=1000):
        """Genera base de clientes usando Spark"""
        print(f"👥 Generando {n} clientes...")
        
        clientes_data = []
        
        for i in range(n):
            edad = np.random.randint(18, 70)
            
            # Segmentación por edad para gasto promedio
            if edad < 25:
                gasto_promedio = np.random.uniform(50, 300)
            elif edad < 40:
                gasto_promedio = np.random.uniform(200, 800)
            elif edad < 55:
                gasto_promedio = np.random.uniform(300, 1200)
            else:
                gasto_promedio = np.random.uniform(100, 600)
            
            clientes_data.append({
                'customer_id': f'C{i:04d}',
                'edad': int(edad),
                'genero': str(np.random.choice(['M', 'F'], p=[0.45, 0.55])),
                'ciudad': str(np.random.choice(self.ciudades)),
                'fecha_registro': pd.date_range('2020-01-01', '2024-01-01', 
                                              periods=n)[i],
                'gasto_promedio': float(gasto_promedio),
                'segmento': str(self.asignar_segmento(gasto_promedio))
            })
        
        # Convertir a Spark DataFrame
        df_pandas = pd.DataFrame(clientes_data)
        df_spark = self.spark.createDataFrame(df_pandas)
        
        return df_spark
    
    def asignar_segmento(self, gasto):
        """Asigna segmento de cliente por gasto"""
        if gasto < 200:
            return 'Bronze'
        elif gasto < 600:
            return 'Silver'
        elif gasto < 1000:
            return 'Gold'
        else:
            return 'Platinum'
    
    def generar_ventas(self, productos_df, clientes_df, n_ventas=5000):
        """Genera transacciones de ventas usando Spark"""
        print(f"💰 Generando {n_ventas} ventas...")
        
        # Convertir Spark DataFrames a pandas para facilitar la generación
        productos_pandas = productos_df.toPandas()
        clientes_pandas = clientes_df.toPandas()
        
        ventas_data = []
        
        # Fechas más recientes tienen más peso
        fechas = pd.date_range('2023-01-01', '2024-08-01', freq='D')
        pesos = np.linspace(0.1, 2.0, len(fechas))  # Más ventas recientes
        
        for i in range(n_ventas):
            # Seleccionar fecha con distribución realista
            fecha = np.random.choice(fechas, p=pesos/pesos.sum())
            
            # Estacionalidad (más ventas en noviembre-diciembre)
            multiplicador_estacional = 1.5 if pd.to_datetime(fecha).month in [11, 12] else 1.0
            if np.random.random() > 0.3 / multiplicador_estacional:
                continue
            
            customer = clientes_pandas.sample(1).iloc[0]
            producto = productos_pandas.sample(1).iloc[0]
            
            # Cantidad basada en precio (productos caros = menos cantidad)
            if producto['precio'] > 500:
                cantidad = np.random.choice([1, 1, 1, 2], p=[0.7, 0.2, 0.08, 0.02])
            else:
                cantidad = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
            
            # Descuento ocasional
            descuento = np.random.choice([0, 0.1, 0.2], p=[0.7, 0.2, 0.1])
            precio_final = producto['precio'] * (1 - descuento)
            
            ventas_data.append({
                'venta_id': f'V{i:05d}',
                'fecha': fecha,
                'customer_id': str(customer['customer_id']),
                'product_id': str(producto['product_id']),
                'cantidad': int(cantidad),
                'precio_unitario': float(producto['precio']),
                'descuento': float(descuento),
                'precio_final': float(precio_final),
                'total': float(precio_final * cantidad),
                'canal': str(np.random.choice(['Online', 'Tienda', 'App'], 
                                        p=[0.6, 0.25, 0.15])),
                'metodo_pago': str(np.random.choice(['Tarjeta', 'PayPal', 'Transferencia'], 
                                              p=[0.5, 0.3, 0.2]))
            })
        
        # Convertir a Spark DataFrame
        df_pandas = pd.DataFrame(ventas_data)
        df_spark = self.spark.createDataFrame(df_pandas)
        
        return df_spark
    
    def generate_all_data(self):
        """Genera todos los datasets y los guarda en formato parquet"""
        print("🚀 Generando todos los datasets...")
        
        # Crear directorio de datos si no existe
        os.makedirs("app/data", exist_ok=True)
        
        # Generar datasets
        productos_df = self.generar_productos(100)
        clientes_df = self.generar_clientes(1000)
        ventas_df = self.generar_ventas(productos_df, clientes_df, 5000)
        
        # Guardar en formato parquet (compatible con Spark)
        productos_df.write.mode("overwrite").parquet("app/data/products.parquet")
        clientes_df.write.mode("overwrite").parquet("app/data/customers.parquet")
        ventas_df.write.mode("overwrite").parquet("app/data/sales.parquet")
        
        print(f"✅ Datasets guardados:")
        print(f"  - Productos: {productos_df.count()} registros")
        print(f"  - Clientes: {clientes_df.count()} registros")
        print(f"  - Ventas: {ventas_df.count()} registros")
        
        return productos_df, clientes_df, ventas_df
    
    def load_data(self):
        """Carga los datasets desde archivos parquet"""
        print("📂 Cargando datasets...")
        
        productos_df = self.spark.read.parquet("app/data/products.parquet")
        clientes_df = self.spark.read.parquet("app/data/customers.parquet")
        ventas_df = self.spark.read.parquet("app/data/sales.parquet")
        
        print(f"✅ Datasets cargados:")
        print(f"  - Productos: {productos_df.count()} registros")
        print(f"  - Clientes: {clientes_df.count()} registros")
        print(f"  - Ventas: {ventas_df.count()} registros")
        
        return productos_df, clientes_df, ventas_df
    
    def get_combined_data(self):
        """Obtiene el dataset combinado para análisis"""
        productos_df, clientes_df, ventas_df = self.load_data()
        
        # Join de los datasets usando Spark
        df_completo = ventas_df.join(
            productos_df, on="product_id", how="inner"
        ).join(
            clientes_df, on="customer_id", how="inner"
        )
        
        # Agregar características temporales
        df_completo = df_completo.withColumn("año", year(col("fecha"))) \
                                .withColumn("mes", month(col("fecha"))) \
                                .withColumn("dia_semana", dayofweek(col("fecha"))) \
                                .withColumn("trimestre", quarter(col("fecha")))
        
        # Calcular métricas
        df_completo = df_completo.withColumn(
            "margen", 
            col("total") - (col("costo") * col("cantidad"))
        ).withColumn(
            "margen_porcentaje", 
            (col("margen") / col("total")) * 100
        )
        
        return df_completo
    
    def stop_spark(self):
        """Detiene la sesión de Spark"""
        if self.spark:
            self.spark.stop()
            print("🛑 Sesión de Spark detenida")

