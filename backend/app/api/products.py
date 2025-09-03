"""
📦 Endpoint de Productos
Análisis de productos, categorías y rendimiento
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta

from app.utils.data_generator import DataGenerator

router = APIRouter()

class ProductResponse(BaseModel):
    """Respuesta del endpoint de productos"""
    product_id: str
    nombre: str
    categoria: str
    precio: float
    ventas_totales: float
    cantidad_vendida: int
    margen_total: float
    margen_porcentaje: float
    num_transacciones: int
    rating_promedio: float
    stock_actual: int

class CategoryResponse(BaseModel):
    """Respuesta del endpoint de categorías"""
    categoria: str
    ventas_totales: float
    margen_total: float
    cantidad_vendida: int
    num_productos: int
    ticket_promedio: float
    productos_top: List[Dict]

@router.get("/products/top", response_model=List[ProductResponse])
async def get_top_products(
    limit: int = Query(10, description="Número de productos a retornar", ge=1, le=50),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    sort_by: str = Query("ventas", description="Ordenar por: ventas, margen, cantidad")
):
    """Obtiene los productos más vendidos"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Filtrar por categoría si se especifica
        if category:
            df_pandas = df_pandas[df_pandas['categoria'] == category]
        
        # Agregar métricas por producto
        productos_metrics = df_pandas.groupby(['product_id', 'nombre', 'categoria', 'precio', 'rating_promedio', 'stock']).agg({
            'total': 'sum',
            'cantidad': 'sum',
            'margen': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Calcular margen porcentaje
        productos_metrics['margen_porcentaje'] = (productos_metrics['margen'] / productos_metrics['total']) * 100
        
        # Ordenar según criterio
        if sort_by == "ventas":
            productos_metrics = productos_metrics.sort_values('total', ascending=False)
        elif sort_by == "margen":
            productos_metrics = productos_metrics.sort_values('margen', ascending=False)
        elif sort_by == "cantidad":
            productos_metrics = productos_metrics.sort_values('cantidad', ascending=False)
        
        # Obtener top N
        top_products = productos_metrics.head(limit)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for _, row in top_products.iterrows():
            response.append(ProductResponse(
                product_id=row['product_id'],
                nombre=row['nombre'],
                categoria=row['categoria'],
                precio=round(row['precio'], 2),
                ventas_totales=round(row['total'], 2),
                cantidad_vendida=int(row['cantidad']),
                margen_total=round(row['margen'], 2),
                margen_porcentaje=round(row['margen_porcentaje'], 2),
                num_transacciones=int(row['venta_id']),
                rating_promedio=round(row['rating_promedio'], 1),
                stock_actual=int(row['stock'])
            ))
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo productos: {str(e)}")

@router.get("/products/categories", response_model=List[CategoryResponse])
async def get_categories_analysis():
    """Obtiene análisis por categorías"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Agregar métricas por categoría
        categorias_metrics = df_pandas.groupby('categoria').agg({
            'total': 'sum',
            'margen': 'sum',
            'cantidad': 'sum',
            'product_id': 'nunique',
            'venta_id': 'count'
        }).reset_index()
        
        # Calcular ticket promedio por categoría
        categorias_metrics['ticket_promedio'] = categorias_metrics['total'] / categorias_metrics['venta_id']
        
        # Ordenar por ventas
        categorias_metrics = categorias_metrics.sort_values('total', ascending=False)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Obtener productos top por categoría
        response = []
        for _, cat_row in categorias_metrics.iterrows():
            categoria = cat_row['categoria']
            
            # Obtener productos top de esta categoría
            productos_cat = df_pandas[df_pandas['categoria'] == categoria]
            top_productos_cat = productos_cat.groupby(['product_id', 'nombre']).agg({
                'total': 'sum'
            }).sort_values('total', ascending=False).head(3)
            
            productos_top_list = []
            for (product_id, nombre), prod_row in top_productos_cat.iterrows():
                productos_top_list.append({
                    'product_id': product_id,
                    'nombre': nombre,
                    'ventas': round(prod_row['total'], 2)
                })
            
            response.append(CategoryResponse(
                categoria=categoria,
                ventas_totales=round(cat_row['total'], 2),
                margen_total=round(cat_row['margen'], 2),
                cantidad_vendida=int(cat_row['cantidad']),
                num_productos=int(cat_row['product_id']),
                ticket_promedio=round(cat_row['ticket_promedio'], 2),
                productos_top=productos_top_list
            ))
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando categorías: {str(e)}")

@router.get("/products/{product_id}")
async def get_product_details(product_id: str):
    """Obtiene detalles específicos de un producto"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Filtrar por producto
        producto_data = df_pandas[df_pandas['product_id'] == product_id]
        
        if producto_data.empty:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Información básica del producto
        producto_info = producto_data.iloc[0]
        
        # Métricas de ventas
        ventas_totales = producto_data['total'].sum()
        cantidad_vendida = producto_data['cantidad'].sum()
        margen_total = producto_data['margen'].sum()
        num_transacciones = len(producto_data)
        
        # Análisis temporal
        ventas_temporales = producto_data.groupby('fecha').agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).reset_index()
        
        # Análisis por canal
        ventas_canal = producto_data.groupby('canal').agg({
            'total': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Análisis por ciudad
        ventas_ciudad = producto_data.groupby('ciudad').agg({
            'total': 'sum',
            'customer_id': 'nunique'
        }).sort_values('total', ascending=False).head(5)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "producto": {
                "product_id": product_id,
                "nombre": producto_info['nombre'],
                "categoria": producto_info['categoria'],
                "precio": round(producto_info['precio'], 2),
                "costo": round(producto_info['costo'], 2),
                "stock": int(producto_info['stock']),
                "rating_promedio": round(producto_info['rating_promedio'], 1),
                "num_reviews": int(producto_info['num_reviews'])
            },
            "metricas_ventas": {
                "ventas_totales": round(ventas_totales, 2),
                "cantidad_vendida": int(cantidad_vendida),
                "margen_total": round(margen_total, 2),
                "margen_porcentaje": round((margen_total / ventas_totales) * 100, 2),
                "num_transacciones": num_transacciones,
                "ticket_promedio": round(ventas_totales / num_transacciones, 2)
            },
            "analisis_temporal": [
                {
                    "fecha": row['fecha'].strftime('%Y-%m-%d'),
                    "ventas": round(row['total'], 2),
                    "cantidad": int(row['cantidad'])
                }
                for _, row in ventas_temporales.iterrows()
            ],
            "analisis_canal": [
                {
                    "canal": row['canal'],
                    "ventas": round(row['total'], 2),
                    "transacciones": int(row['venta_id'])
                }
                for _, row in ventas_canal.iterrows()
            ],
            "top_ciudades": [
                {
                    "ciudad": ciudad,
                    "ventas": round(ventas, 2),
                    "clientes": int(clientes)
                }
                for ciudad, (ventas, clientes) in ventas_ciudad.iterrows()
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalles del producto: {str(e)}")

@router.get("/products/performance/trends")
async def get_products_performance_trends():
    """Obtiene tendencias de rendimiento de productos"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis de rendimiento por mes
        ventas_mensuales = df_pandas.groupby(['año', 'mes', 'product_id', 'nombre']).agg({
            'total': 'sum',
            'cantidad': 'sum',
            'margen': 'sum'
        }).reset_index()
        
        # Calcular crecimiento de productos
        productos_crecimiento = []
        for product_id in df_pandas['product_id'].unique():
            producto_data = ventas_mensuales[ventas_mensuales['product_id'] == product_id]
            if len(producto_data) >= 2:
                # Ordenar por fecha
                producto_data['fecha'] = pd.to_datetime(
                    producto_data['año'].astype(str) + '-' + 
                    producto_data['mes'].astype(str) + '-01'
                )
                producto_data = producto_data.sort_values('fecha')
                
                # Calcular crecimiento
                ventas_actual = producto_data.iloc[-1]['total']
                ventas_anterior = producto_data.iloc[-2]['total']
                
                if ventas_anterior > 0:
                    crecimiento = ((ventas_actual - ventas_anterior) / ventas_anterior) * 100
                else:
                    crecimiento = 0
                
                productos_crecimiento.append({
                    'product_id': product_id,
                    'nombre': producto_data.iloc[-1]['nombre'],
                    'ventas_actual': round(ventas_actual, 2),
                    'crecimiento_porcentual': round(crecimiento, 2)
                })
        
        # Ordenar por crecimiento
        productos_crecimiento.sort(key=lambda x: x['crecimiento_porcentual'], reverse=True)
        
        # Análisis de categorías por rendimiento
        categorias_rendimiento = df_pandas.groupby('categoria').agg({
            'total': 'sum',
            'margen': 'sum',
            'product_id': 'nunique'
        }).reset_index()
        
        categorias_rendimiento['margen_porcentaje'] = (categorias_rendimiento['margen'] / categorias_rendimiento['total']) * 100
        categorias_rendimiento['ventas_por_producto'] = categorias_rendimiento['total'] / categorias_rendimiento['product_id']
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "productos_crecimiento": productos_crecimiento[:10],  # Top 10
            "categorias_rendimiento": [
                {
                    "categoria": row['categoria'],
                    "ventas_totales": round(row['total'], 2),
                    "margen_porcentaje": round(row['margen_porcentaje'], 2),
                    "ventas_por_producto": round(row['ventas_por_producto'], 2),
                    "num_productos": int(row['product_id'])
                }
                for _, row in categorias_rendimiento.iterrows()
            ],
            "insights": {
                "producto_mas_crecimiento": productos_crecimiento[0] if productos_crecimiento else None,
                "categoria_mas_rentable": categorias_rendimiento.loc[categorias_rendimiento['margen_porcentaje'].idxmax()]['categoria'] if not categorias_rendimiento.empty else None,
                "total_productos_analizados": len(productos_crecimiento)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando tendencias: {str(e)}")

@router.get("/products/inventory/analysis")
async def get_inventory_analysis():
    """Obtiene análisis de inventario y stock"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis de inventario
        inventario_analysis = df_pandas.groupby(['product_id', 'nombre', 'categoria', 'stock']).agg({
            'cantidad': 'sum',
            'total': 'sum'
        }).reset_index()
        
        # Calcular métricas de inventario
        inventario_analysis['rotacion'] = inventario_analysis['cantidad'] / inventario_analysis['stock'].replace(0, 1)
        inventario_analysis['valor_inventario'] = inventario_analysis['stock'] * inventario_analysis['total'] / inventario_analysis['cantidad'].replace(0, 1)
        
        # Clasificar productos por rotación
        def clasificar_rotacion(rotacion):
            if rotacion > 10:
                return "Alta"
            elif rotacion > 5:
                return "Media"
            else:
                return "Baja"
        
        inventario_analysis['clasificacion_rotacion'] = inventario_analysis['rotacion'].apply(clasificar_rotacion)
        
        # Productos con bajo stock
        productos_bajo_stock = inventario_analysis[inventario_analysis['stock'] < 10].sort_values('total', ascending=False)
        
        # Productos con alta rotación
        productos_alta_rotacion = inventario_analysis[inventario_analysis['rotacion'] > 10].sort_values('rotacion', ascending=False)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "resumen_inventario": {
                "total_productos": len(inventario_analysis),
                "valor_total_inventario": round(inventario_analysis['valor_inventario'].sum(), 2),
                "rotacion_promedio": round(inventario_analysis['rotacion'].mean(), 2),
                "productos_bajo_stock": len(productos_bajo_stock),
                "productos_alta_rotacion": len(productos_alta_rotacion)
            },
            "productos_bajo_stock": [
                {
                    "product_id": row['product_id'],
                    "nombre": row['nombre'],
                    "categoria": row['categoria'],
                    "stock_actual": int(row['stock']),
                    "ventas_totales": round(row['total'], 2)
                }
                for _, row in productos_bajo_stock.head(10).iterrows()
            ],
            "productos_alta_rotacion": [
                {
                    "product_id": row['product_id'],
                    "nombre": row['nombre'],
                    "categoria": row['categoria'],
                    "rotacion": round(row['rotacion'], 2),
                    "stock_actual": int(row['stock'])
                }
                for _, row in productos_alta_rotacion.head(10).iterrows()
            ],
            "clasificacion_por_rotacion": {
                "alta": int((inventario_analysis['clasificacion_rotacion'] == "Alta").sum()),
                "media": int((inventario_analysis['clasificacion_rotacion'] == "Media").sum()),
                "baja": int((inventario_analysis['clasificacion_rotacion'] == "Baja").sum())
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando inventario: {str(e)}")

