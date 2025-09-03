"""
👥 Endpoint de Clientes
Análisis RFM, segmentación y comportamiento de clientes
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta

from app.utils.data_generator import DataGenerator

router = APIRouter()

class CustomerRFMResponse(BaseModel):
    """Respuesta del endpoint de análisis RFM"""
    customer_id: str
    recency: int
    frequency: int
    monetary: float
    rfm_score: str
    segment: str

class CustomerSegmentResponse(BaseModel):
    """Respuesta del endpoint de segmentación"""
    segmento: str
    num_clientes: int
    ventas_totales: float
    ticket_promedio: float
    frecuencia_promedio: float
    clientes_top: List[Dict]

@router.get("/customers/rfm", response_model=List[CustomerRFMResponse])
async def get_customers_rfm(
    limit: int = Query(50, description="Número de clientes a retornar", ge=1, le=100),
    segment: Optional[str] = Query(None, description="Filtrar por segmento RFM")
):
    """Obtiene análisis RFM de clientes"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Calcular RFM
        fecha_max = df_pandas['fecha'].max()
        
        rfm = df_pandas.groupby('customer_id').agg({
            'fecha': lambda x: (fecha_max - x.max()).days,  # Recency
            'venta_id': 'count',  # Frequency
            'total': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        # Calcular quintiles para RFM
        rfm['R_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
        rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfm['M_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
        
        # Combinar scores
        rfm['RFM_Score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)
        
        # Asignar segmentos
        def asignar_segmento_rfm(rfm_score):
            if rfm_score >= '444':
                return 'Champions'
            elif rfm_score >= '333':
                return 'Loyal Customers'
            elif rfm_score >= '222':
                return 'At Risk'
            elif rfm_score >= '111':
                return 'Can\'t Lose'
            else:
                return 'Lost'
        
        rfm['segment'] = rfm['RFM_Score'].apply(asignar_segmento_rfm)
        
        # Filtrar por segmento si se especifica
        if segment:
            rfm = rfm[rfm['segment'] == segment]
        
        # Ordenar por valor monetario
        rfm = rfm.sort_values('monetary', ascending=False).head(limit)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for _, row in rfm.iterrows():
            response.append(CustomerRFMResponse(
                customer_id=row['customer_id'],
                recency=int(row['recency']),
                frequency=int(row['frequency']),
                monetary=round(row['monetary'], 2),
                rfm_score=row['RFM_Score'],
                segment=row['segment']
            ))
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo análisis RFM: {str(e)}")

@router.get("/customers/segments", response_model=List[CustomerSegmentResponse])
async def get_customers_segments():
    """Obtiene análisis de segmentación de clientes"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis por segmento
        segmentos_analysis = df_pandas.groupby('segmento').agg({
            'customer_id': 'nunique',
            'total': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        segmentos_analysis.columns = ['segmento', 'num_clientes', 'ventas_totales', 'num_transacciones']
        
        # Calcular métricas adicionales
        segmentos_analysis['ticket_promedio'] = segmentos_analysis['ventas_totales'] / segmentos_analysis['num_transacciones']
        segmentos_analysis['frecuencia_promedio'] = segmentos_analysis['num_transacciones'] / segmentos_analysis['num_clientes']
        
        # Ordenar por ventas totales
        segmentos_analysis = segmentos_analysis.sort_values('ventas_totales', ascending=False)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Obtener clientes top por segmento
        response = []
        for _, seg_row in segmentos_analysis.iterrows():
            segmento = seg_row['segmento']
            
            # Obtener clientes top de este segmento
            clientes_segmento = df_pandas[df_pandas['segmento'] == segmento]
            top_clientes = clientes_segmento.groupby('customer_id').agg({
                'total': 'sum',
                'venta_id': 'count'
            }).sort_values('total', ascending=False).head(5)
            
            clientes_top_list = []
            for customer_id, cli_row in top_clientes.iterrows():
                clientes_top_list.append({
                    'customer_id': customer_id,
                    'ventas_totales': round(cli_row['total'], 2),
                    'num_transacciones': int(cli_row['venta_id'])
                })
            
            response.append(CustomerSegmentResponse(
                segmento=segmento,
                num_clientes=int(seg_row['num_clientes']),
                ventas_totales=round(seg_row['ventas_totales'], 2),
                ticket_promedio=round(seg_row['ticket_promedio'], 2),
                frecuencia_promedio=round(seg_row['frecuencia_promedio'], 2),
                clientes_top=clientes_top_list
            ))
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando segmentos: {str(e)}")

@router.get("/customers/{customer_id}")
async def get_customer_details(customer_id: str):
    """Obtiene detalles específicos de un cliente"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Filtrar por cliente
        cliente_data = df_pandas[df_pandas['customer_id'] == customer_id]
        
        if cliente_data.empty:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        # Información básica del cliente
        cliente_info = cliente_data.iloc[0]
        
        # Métricas de compra
        ventas_totales = cliente_data['total'].sum()
        num_transacciones = len(cliente_data)
        cantidad_total = cliente_data['cantidad'].sum()
        margen_total = cliente_data['margen'].sum()
        
        # Calcular RFM
        fecha_max = df_pandas['fecha'].max()
        recency = (fecha_max - cliente_data['fecha'].max()).days
        frequency = num_transacciones
        monetary = ventas_totales
        
        # Análisis temporal de compras
        compras_temporales = cliente_data.groupby('fecha').agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).reset_index()
        
        # Análisis por categoría
        compras_categoria = cliente_data.groupby('categoria').agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).sort_values('total', ascending=False)
        
        # Análisis por canal
        compras_canal = cliente_data.groupby('canal').agg({
            'total': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Productos favoritos
        productos_favoritos = cliente_data.groupby(['product_id', 'nombre']).agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).sort_values('total', ascending=False).head(5)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "cliente": {
                "customer_id": customer_id,
                "edad": int(cliente_info['edad']),
                "genero": cliente_info['genero'],
                "ciudad": cliente_info['ciudad'],
                "segmento": cliente_info['segmento'],
                "fecha_registro": cliente_info['fecha_registro'].strftime('%Y-%m-%d')
            },
            "metricas_compras": {
                "ventas_totales": round(ventas_totales, 2),
                "num_transacciones": num_transacciones,
                "cantidad_total": int(cantidad_total),
                "margen_total": round(margen_total, 2),
                "ticket_promedio": round(ventas_totales / num_transacciones, 2),
                "frecuencia_compras": round(num_transacciones / ((fecha_max - cliente_info['fecha_registro']).days / 30), 2)
            },
            "analisis_rfm": {
                "recency": int(recency),
                "frequency": int(frequency),
                "monetary": round(monetary, 2),
                "valor_cliente": "Alto" if monetary > 1000 else "Medio" if monetary > 500 else "Bajo"
            },
            "compras_temporales": [
                {
                    "fecha": row['fecha'].strftime('%Y-%m-%d'),
                    "ventas": round(row['total'], 2),
                    "cantidad": int(row['cantidad'])
                }
                for _, row in compras_temporales.iterrows()
            ],
            "compras_categoria": [
                {
                    "categoria": categoria,
                    "ventas": round(ventas, 2),
                    "cantidad": int(cantidad)
                }
                for categoria, (ventas, cantidad) in compras_categoria.iterrows()
            ],
            "compras_canal": [
                {
                    "canal": row['canal'],
                    "ventas": round(row['total'], 2),
                    "transacciones": int(row['venta_id'])
                }
                for _, row in compras_canal.iterrows()
            ],
            "productos_favoritos": [
                {
                    "product_id": product_id,
                    "nombre": nombre,
                    "ventas": round(ventas, 2),
                    "cantidad": int(cantidad)
                }
                for (product_id, nombre), (ventas, cantidad) in productos_favoritos.iterrows()
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalles del cliente: {str(e)}")

@router.get("/customers/behavior/analysis")
async def get_customer_behavior_analysis():
    """Obtiene análisis de comportamiento de clientes"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis de comportamiento por edad
        comportamiento_edad = df_pandas.groupby('edad').agg({
            'total': 'sum',
            'customer_id': 'nunique',
            'venta_id': 'count'
        }).reset_index()
        
        comportamiento_edad['ticket_promedio'] = comportamiento_edad['total'] / comportamiento_edad['venta_id']
        comportamiento_edad['frecuencia_promedio'] = comportamiento_edad['venta_id'] / comportamiento_edad['customer_id']
        
        # Análisis por género
        comportamiento_genero = df_pandas.groupby('genero').agg({
            'total': 'sum',
            'customer_id': 'nunique',
            'venta_id': 'count'
        }).reset_index()
        
        comportamiento_genero['ticket_promedio'] = comportamiento_genero['total'] / comportamiento_genero['venta_id']
        
        # Análisis por ciudad
        comportamiento_ciudad = df_pandas.groupby('ciudad').agg({
            'total': 'sum',
            'customer_id': 'nunique',
            'venta_id': 'count'
        }).reset_index()
        
        comportamiento_ciudad['ticket_promedio'] = comportamiento_ciudad['total'] / comportamiento_ciudad['venta_id']
        comportamiento_ciudad = comportamiento_ciudad.sort_values('total', ascending=False)
        
        # Análisis de lealtad (clientes que compran múltiples veces)
        lealtad_clientes = df_pandas.groupby('customer_id').agg({
            'venta_id': 'count',
            'total': 'sum'
        }).reset_index()
        
        lealtad_clientes.columns = ['customer_id', 'num_compras', 'ventas_totales']
        
        # Clasificar por lealtad
        def clasificar_lealtad(num_compras):
            if num_compras >= 10:
                return "Muy Leal"
            elif num_compras >= 5:
                return "Leal"
            elif num_compras >= 2:
                return "Ocasional"
            else:
                return "Nuevo"
        
        lealtad_clientes['tipo_lealtad'] = lealtad_clientes['num_compras'].apply(clasificar_lealtad)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "comportamiento_edad": [
                {
                    "edad": int(row['edad']),
                    "ventas_totales": round(row['total'], 2),
                    "num_clientes": int(row['customer_id']),
                    "ticket_promedio": round(row['ticket_promedio'], 2),
                    "frecuencia_promedio": round(row['frecuencia_promedio'], 2)
                }
                for _, row in comportamiento_edad.iterrows()
            ],
            "comportamiento_genero": [
                {
                    "genero": row['genero'],
                    "ventas_totales": round(row['total'], 2),
                    "num_clientes": int(row['customer_id']),
                    "ticket_promedio": round(row['ticket_promedio'], 2)
                }
                for _, row in comportamiento_genero.iterrows()
            ],
            "top_ciudades": [
                {
                    "ciudad": row['ciudad'],
                    "ventas_totales": round(row['total'], 2),
                    "num_clientes": int(row['customer_id']),
                    "ticket_promedio": round(row['ticket_promedio'], 2)
                }
                for _, row in comportamiento_ciudad.head(10).iterrows()
            ],
            "analisis_lealtad": {
                "muy_leal": int((lealtad_clientes['tipo_lealtad'] == "Muy Leal").sum()),
                "leal": int((lealtad_clientes['tipo_lealtad'] == "Leal").sum()),
                "ocasional": int((lealtad_clientes['tipo_lealtad'] == "Ocasional").sum()),
                "nuevo": int((lealtad_clientes['tipo_lealtad'] == "Nuevo").sum())
            },
            "insights": {
                "edad_promedio": round(comportamiento_edad['edad'].mean(), 1),
                "edad_max_ventas": int(comportamiento_edad.loc[comportamiento_edad['total'].idxmax()]['edad']),
                "genero_dominante": comportamiento_genero.loc[comportamiento_genero['total'].idxmax()]['genero'],
                "ciudad_top": comportamiento_ciudad.iloc[0]['ciudad'] if not comportamiento_ciudad.empty else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando comportamiento: {str(e)}")

@router.get("/customers/retention/analysis")
async def get_customer_retention_analysis():
    """Obtiene análisis de retención de clientes"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis de cohortes por mes de primera compra
        df_pandas['fecha_compra'] = pd.to_datetime(df_pandas['fecha'])
        df_pandas['periodo_compra'] = df_pandas['fecha_compra'].dt.to_period('M')
        
        # Primera compra por cliente
        primera_compra = df_pandas.groupby('customer_id')['fecha_compra'].min().reset_index()
        primera_compra.columns = ['customer_id', 'cohorte_fecha']
        primera_compra['cohorte_periodo'] = primera_compra['cohorte_fecha'].dt.to_period('M')
        
        # Mergear con datos originales
        df_cohorte = df_pandas.merge(primera_compra, on='customer_id')
        df_cohorte['periodo_numero'] = (df_cohorte['periodo_compra'] - df_cohorte['cohorte_periodo']).apply(lambda x: x.n)
        
        # Tabla de cohortes
        tabla_cohortes = df_cohorte.groupby(['cohorte_periodo', 'periodo_numero'])['customer_id'].nunique().reset_index()
        tabla_cohortes_pivot = tabla_cohortes.pivot(index='cohorte_periodo', 
                                                   columns='periodo_numero', 
                                                   values='customer_id')
        
        # Tamaño de cohortes
        tamanos_cohorte = primera_compra.groupby('cohorte_periodo').size()
        
        # Tasa de retención
        tabla_retencion = tabla_cohortes_pivot.divide(tamanos_cohorte, axis=0)
        
        # Análisis de churn
        fecha_max = df_pandas['fecha'].max()
        fecha_limite = fecha_max - timedelta(days=90)  # 3 meses sin comprar
        
        clientes_activos = df_pandas[df_pandas['fecha'] >= fecha_limite]['customer_id'].nunique()
        clientes_totales = df_pandas['customer_id'].nunique()
        tasa_actividad = clientes_activos / clientes_totales
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "tasa_retencion": {
                "cohortes": [
                    {
                        "cohorte": str(cohorte),
                        "tasa_retencion": [
                            {
                                "mes": int(mes),
                                "tasa": round(tasa, 3) if not pd.isna(tasa) else 0
                            }
                            for mes, tasa in row.items()
                        ]
                    }
                    for cohorte, row in tabla_retencion.iterrows()
                ]
            },
            "analisis_churn": {
                "clientes_activos": clientes_activos,
                "clientes_totales": clientes_totales,
                "tasa_actividad": round(tasa_actividad * 100, 2),
                "tasa_churn": round((1 - tasa_actividad) * 100, 2),
                "periodo_analisis": "3 meses"
            },
            "cohortes_resumen": {
                "total_cohortes": len(tabla_retencion),
                "cohorte_mas_grande": str(tamanos_cohorte.idxmax()) if not tamanos_cohorte.empty else None,
                "cohorte_mas_pequena": str(tamanos_cohorte.idxmin()) if not tamanos_cohorte.empty else None,
                "tamaño_promedio_cohorte": round(tamanos_cohorte.mean(), 1)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando retención: {str(e)}")

