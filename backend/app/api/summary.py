"""
📊 Endpoint de Resumen General
Proporciona métricas clave del negocio
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta

from app.utils.data_generator import DataGenerator
from app.utils.database import get_spark_session

router = APIRouter()

class SummaryResponse(BaseModel):
    """Respuesta del endpoint de resumen"""
    total_ventas: float
    total_margen: float
    margen_porcentaje: float
    num_clientes: int
    num_productos: int
    ticket_promedio: float
    ventas_mensuales: List[Dict]
    top_categorias: List[Dict]
    top_ciudades: List[Dict]
    canales_venta: List[Dict]
    ultima_actualizacion: str

@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """Obtiene resumen general del negocio"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Convertir a pandas para análisis
        df_pandas = df_completo.toPandas()
        
        # Métricas principales
        total_ventas = df_pandas['total'].sum()
        total_margen = df_pandas['margen'].sum()
        margen_porcentaje = (total_margen / total_ventas) * 100
        num_clientes = df_pandas['customer_id'].nunique()
        num_productos = df_pandas['product_id'].nunique()
        ticket_promedio = df_pandas['total'].mean()
        
        # Ventas mensuales (últimos 6 meses)
        ventas_mensuales = df_pandas.groupby(['año', 'mes']).agg({
            'total': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Ordenar por fecha y obtener últimos 6 meses
        ventas_mensuales['fecha'] = pd.to_datetime(
            ventas_mensuales['año'].astype(str) + '-' + 
            ventas_mensuales['mes'].astype(str) + '-01'
        )
        ventas_mensuales = ventas_mensuales.sort_values('fecha').tail(6)
        
        ventas_mensuales_list = []
        for _, row in ventas_mensuales.iterrows():
            ventas_mensuales_list.append({
                'fecha': f"{row['año']}-{row['mes']:02d}",
                'ventas': round(row['total'], 2),
                'transacciones': int(row['venta_id'])
            })
        
        # Top categorías
        top_categorias = df_pandas.groupby('categoria').agg({
            'total': 'sum',
            'margen': 'sum',
            'cantidad': 'sum'
        }).sort_values('total', ascending=False).head(5)
        
        top_categorias_list = []
        for categoria, row in top_categorias.iterrows():
            top_categorias_list.append({
                'categoria': categoria,
                'ventas': round(row['total'], 2),
                'margen': round(row['margen'], 2),
                'cantidad': int(row['cantidad'])
            })
        
        # Top ciudades
        top_ciudades = df_pandas.groupby('ciudad').agg({
            'total': 'sum',
            'customer_id': 'nunique'
        }).sort_values('total', ascending=False).head(5)
        
        top_ciudades_list = []
        for ciudad, row in top_ciudades.iterrows():
            top_ciudades_list.append({
                'ciudad': ciudad,
                'ventas': round(row['total'], 2),
                'clientes': int(row['customer_id'])
            })
        
        # Canales de venta
        canales_venta = df_pandas.groupby('canal').agg({
            'total': 'sum',
            'venta_id': 'count'
        }).sort_values('total', ascending=False)
        
        canales_venta_list = []
        for canal, row in canales_venta.iterrows():
            canales_venta_list.append({
                'canal': canal,
                'ventas': round(row['total'], 2),
                'transacciones': int(row['venta_id'])
            })
        
        # Detener Spark para liberar recursos
        data_generator.stop_spark()
        
        return SummaryResponse(
            total_ventas=round(total_ventas, 2),
            total_margen=round(total_margen, 2),
            margen_porcentaje=round(margen_porcentaje, 2),
            num_clientes=num_clientes,
            num_productos=num_productos,
            ticket_promedio=round(ticket_promedio, 2),
            ventas_mensuales=ventas_mensuales_list,
            top_categorias=top_categorias_list,
            top_ciudades=top_ciudades_list,
            canales_venta=canales_venta_list,
            ultima_actualizacion=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo resumen: {str(e)}")

@router.get("/summary/metrics")
async def get_key_metrics():
    """Obtiene métricas clave en formato simplificado"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Calcular métricas
        total_ventas = df_pandas['total'].sum()
        total_margen = df_pandas['margen'].sum()
        num_clientes = df_pandas['customer_id'].nunique()
        ticket_promedio = df_pandas['total'].mean()
        
        # Crecimiento vs mes anterior
        ventas_mensuales = df_pandas.groupby(['año', 'mes'])['total'].sum().reset_index()
        ventas_mensuales['fecha'] = pd.to_datetime(
            ventas_mensuales['año'].astype(str) + '-' + 
            ventas_mensuales['mes'].astype(str) + '-01'
        )
        ventas_mensuales = ventas_mensuales.sort_values('fecha')
        
        if len(ventas_mensuales) >= 2:
            mes_actual = ventas_mensuales.iloc[-1]['total']
            mes_anterior = ventas_mensuales.iloc[-2]['total']
            crecimiento = ((mes_actual - mes_anterior) / mes_anterior) * 100
        else:
            crecimiento = 0
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "total_ventas": round(total_ventas, 2),
            "total_margen": round(total_margen, 2),
            "num_clientes": num_clientes,
            "ticket_promedio": round(ticket_promedio, 2),
            "crecimiento_mensual": round(crecimiento, 2),
            "margen_porcentaje": round((total_margen / total_ventas) * 100, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo métricas: {str(e)}")

@router.get("/summary/dashboard")
async def get_dashboard_data():
    """Obtiene datos para el dashboard principal"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Ventas por día (últimos 30 días)
        fecha_max = df_pandas['fecha'].max()
        fecha_min = fecha_max - timedelta(days=30)
        
        ventas_diarias = df_pandas[
            df_pandas['fecha'] >= fecha_min
        ].groupby('fecha').agg({
            'total': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Rellenar fechas faltantes
        date_range = pd.date_range(start=fecha_min, end=fecha_max, freq='D')
        complete_df = pd.DataFrame({'fecha': date_range})
        ventas_diarias = complete_df.merge(ventas_diarias, on='fecha', how='left').fillna(0)
        
        ventas_diarias_list = []
        for _, row in ventas_diarias.iterrows():
            ventas_diarias_list.append({
                'fecha': row['fecha'].strftime('%Y-%m-%d'),
                'ventas': round(row['total'], 2),
                'transacciones': int(row['venta_id'])
            })
        
        # Top productos
        top_productos = df_pandas.groupby(['product_id', 'nombre']).agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).sort_values('total', ascending=False).head(10)
        
        top_productos_list = []
        for (product_id, nombre), row in top_productos.iterrows():
            top_productos_list.append({
                'product_id': product_id,
                'nombre': nombre,
                'ventas': round(row['total'], 2),
                'cantidad': int(row['cantidad'])
            })
        
        # Distribución por segmento
        segmentos = df_pandas.groupby('segmento').agg({
            'total': 'sum',
            'customer_id': 'nunique'
        }).sort_values('total', ascending=False)
        
        segmentos_list = []
        for segmento, row in segmentos.iterrows():
            segmentos_list.append({
                'segmento': segmento,
                'ventas': round(row['total'], 2),
                'clientes': int(row['customer_id'])
            })
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "ventas_diarias": ventas_diarias_list,
            "top_productos": top_productos_list,
            "segmentos": segmentos_list,
            "periodo": {
                "inicio": fecha_min.strftime('%Y-%m-%d'),
                "fin": fecha_max.strftime('%Y-%m-%d')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos del dashboard: {str(e)}")

