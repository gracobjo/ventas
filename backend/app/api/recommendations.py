"""
🎯 Endpoint de Recomendaciones
Sistema híbrido de recomendaciones colaborativo + content-based
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

from app.utils.data_generator import DataGenerator
from app.ml.recommendations import RecommendationSystem

router = APIRouter()

class RecommendationResponse(BaseModel):
    """Respuesta del endpoint de recomendaciones"""
    product_id: str
    nombre: str
    categoria: str
    precio: float
    score: float
    tipo_recomendacion: str

class SimilarProductResponse(BaseModel):
    """Respuesta del endpoint de productos similares"""
    product_id: str
    nombre: str
    categoria: str
    precio: float
    similitud: float

@router.get("/recommendations/{customer_id}", response_model=List[RecommendationResponse])
async def get_customer_recommendations(
    customer_id: str,
    limit: int = Query(5, description="Número de recomendaciones", ge=1, le=20),
    recommendation_type: str = Query("hybrid", description="Tipo: hybrid, collaborative, content")
):
    """Obtiene recomendaciones personalizadas para un cliente"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar sistema de recomendaciones
        rec_system = RecommendationSystem()
        
        # Intentar cargar modelos existentes
        try:
            rec_system.load_models()
            print("✅ Modelos de recomendaciones cargados")
        except:
            print("🔄 Entrenando nuevos modelos de recomendaciones...")
            # Entrenar modelo híbrido
            rec_system.train_hybrid_model(df_completo, productos_df)
            rec_system.save_models()
        
        # Obtener recomendaciones según tipo
        if recommendation_type == "hybrid":
            recommendations, status = rec_system.get_hybrid_recommendations(customer_id, limit)
            tipo = "Híbrido"
        elif recommendation_type == "collaborative":
            recommendations, status = rec_system.get_collaborative_recommendations(customer_id, limit)
            tipo = "Colaborativo"
        elif recommendation_type == "content":
            recommendations, status = rec_system.get_content_based_recommendations(customer_id, limit)
            tipo = "Content-Based"
        else:
            raise HTTPException(status_code=400, detail="Tipo de recomendación no válido")
        
        if status != "Éxito":
            raise HTTPException(status_code=404, detail=status)
        
        # Obtener información de productos
        productos_pandas = productos_df.toPandas()
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for product_id, score in recommendations:
            # Buscar información del producto
            producto_info = productos_pandas[productos_pandas['product_id'] == product_id]
            if not producto_info.empty:
                producto = producto_info.iloc[0]
                response.append(RecommendationResponse(
                    product_id=product_id,
                    nombre=producto['nombre'],
                    categoria=producto['categoria'],
                    precio=round(producto['precio'], 2),
                    score=round(score, 3),
                    tipo_recomendacion=tipo
                ))
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo recomendaciones: {str(e)}")

@router.get("/recommendations/products/{product_id}/similar", response_model=List[SimilarProductResponse])
async def get_similar_products(
    product_id: str,
    limit: int = Query(5, description="Número de productos similares", ge=1, le=20)
):
    """Obtiene productos similares a uno dado"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar sistema de recomendaciones
        rec_system = RecommendationSystem()
        
        # Cargar modelos existentes
        try:
            rec_system.load_models()
        except:
            # Entrenar modelo si no existe
            rec_system.train_hybrid_model(df_completo, productos_df)
            rec_system.save_models()
        
        # Obtener productos similares
        similar_products, status = rec_system.get_similar_products(product_id, limit)
        
        if status != "Éxito":
            raise HTTPException(status_code=404, detail=status)
        
        # Obtener información de productos
        productos_pandas = productos_df.toPandas()
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for similar_product_id, similarity in similar_products:
            # Buscar información del producto
            producto_info = productos_pandas[productos_pandas['product_id'] == similar_product_id]
            if not producto_info.empty:
                producto = producto_info.iloc[0]
                response.append(SimilarProductResponse(
                    product_id=similar_product_id,
                    nombre=producto['nombre'],
                    categoria=producto['categoria'],
                    precio=round(producto['precio'], 2),
                    similitud=round(similarity, 3)
                ))
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo productos similares: {str(e)}")

@router.get("/recommendations/system/stats")
async def get_recommendation_system_stats():
    """Obtiene estadísticas del sistema de recomendaciones"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar sistema de recomendaciones
        rec_system = RecommendationSystem()
        
        # Cargar modelos existentes
        try:
            rec_system.load_models()
        except:
            # Entrenar modelo si no existe
            rec_system.train_hybrid_model(df_completo, productos_df)
            rec_system.save_models()
        
        # Obtener estadísticas
        stats = rec_system.get_system_stats()
        
        # Detener Spark
        data_generator.stop_spark()
        
        if stats:
            return {
                "estadisticas_sistema": {
                    "num_usuarios": stats['num_users'],
                    "num_productos": stats['num_products'],
                    "densidad_matriz": round(stats['matrix_density'] * 100, 2),
                    "ratings_promedio_usuario": round(stats['avg_ratings_per_user'], 2),
                    "ratings_promedio_producto": round(stats['avg_ratings_per_product'], 2)
                },
                "configuracion": {
                    "pesos_hibridos": rec_system.hybrid_weights,
                    "modelo_principal": "Híbrido (Collaborative + Content-Based)"
                },
                "ultima_actualizacion": datetime.now().isoformat()
            }
        else:
            return {
                "estadisticas_sistema": "No disponible",
                "configuracion": {
                    "pesos_hibridos": rec_system.hybrid_weights,
                    "modelo_principal": "Híbrido (Collaborative + Content-Based)"
                },
                "ultima_actualizacion": datetime.now().isoformat()
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.get("/recommendations/evaluation")
async def evaluate_recommendation_system():
    """Evalúa la calidad del sistema de recomendaciones"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar sistema de recomendaciones
        rec_system = RecommendationSystem()
        
        # Cargar modelos existentes
        try:
            rec_system.load_models()
        except:
            # Entrenar modelo si no existe
            rec_system.train_hybrid_model(df_completo, productos_df)
            rec_system.save_models()
        
        # Evaluar sistema
        evaluation = rec_system.evaluate_recommendations(n_test=50)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "evaluacion_modelos": {
                "collaborative": {
                    "precision": round(evaluation['collaborative']['precision'], 3),
                    "recall": round(evaluation['collaborative']['recall'], 3),
                    "f1_score": round(evaluation['collaborative']['f1_score'], 3)
                },
                "content": {
                    "precision": round(evaluation['content']['precision'], 3),
                    "recall": round(evaluation['content']['recall'], 3),
                    "f1_score": round(evaluation['content']['f1_score'], 3)
                },
                "hybrid": {
                    "precision": round(evaluation['hybrid']['precision'], 3),
                    "recall": round(evaluation['hybrid']['recall'], 3),
                    "f1_score": round(evaluation['hybrid']['f1_score'], 3)
                }
            },
            "mejor_modelo": max(evaluation.items(), key=lambda x: x[1]['f1_score'])[0],
            "resumen_evaluacion": {
                "total_usuarios_evaluados": 50,
                "metrica_principal": "F1-Score",
                "umbral_evaluacion": "Leave-one-out"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluando sistema: {str(e)}")

@router.get("/recommendations/popular")
async def get_popular_recommendations(
    limit: int = Query(10, description="Número de productos populares", ge=1, le=50),
    category: Optional[str] = Query(None, description="Filtrar por categoría")
):
    """Obtiene productos populares basados en ventas"""
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
        
        # Calcular popularidad basada en ventas
        popular_products = df_pandas.groupby(['product_id', 'nombre', 'categoria', 'precio']).agg({
            'total': 'sum',
            'cantidad': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        
        # Calcular score de popularidad
        popular_products['popularity_score'] = (
            popular_products['total'] * 0.5 +  # Ventas totales
            popular_products['cantidad'] * 0.3 +  # Cantidad vendida
            popular_products['customer_id'] * 0.2  # Número de clientes únicos
        )
        
        # Ordenar por popularidad
        popular_products = popular_products.sort_values('popularity_score', ascending=False).head(limit)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for _, row in popular_products.iterrows():
            response.append({
                "product_id": row['product_id'],
                "nombre": row['nombre'],
                "categoria": row['categoria'],
                "precio": round(row['precio'], 2),
                "ventas_totales": round(row['total'], 2),
                "cantidad_vendida": int(row['cantidad']),
                "clientes_unicos": int(row['customer_id']),
                "popularity_score": round(row['popularity_score'], 2)
            })
        
        return {
            "productos_populares": response,
            "categoria_filtro": category,
            "total_productos": len(response)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo productos populares: {str(e)}")

@router.get("/recommendations/trending")
async def get_trending_recommendations(
    days: int = Query(30, description="Período de análisis en días", ge=7, le=90),
    limit: int = Query(10, description="Número de productos trending", ge=1, le=50)
):
    """Obtiene productos trending basados en crecimiento reciente"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Calcular fechas de análisis
        fecha_max = df_pandas['fecha'].max()
        fecha_inicio = fecha_max - pd.Timedelta(days=days)
        fecha_mitad = fecha_max - pd.Timedelta(days=days//2)
        
        # Ventas en período reciente
        ventas_recientes = df_pandas[df_pandas['fecha'] >= fecha_mitad].groupby('product_id').agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).reset_index()
        
        # Ventas en período anterior
        ventas_anteriores = df_pandas[
            (df_pandas['fecha'] >= fecha_inicio) & 
            (df_pandas['fecha'] < fecha_mitad)
        ].groupby('product_id').agg({
            'total': 'sum',
            'cantidad': 'sum'
        }).reset_index()
        
        # Calcular crecimiento
        trending_products = ventas_recientes.merge(
            ventas_anteriores, 
            on='product_id', 
            how='left', 
            suffixes=('_reciente', '_anterior')
        ).fillna(0)
        
        # Calcular métricas de crecimiento
        trending_products['crecimiento_ventas'] = (
            trending_products['total_reciente'] - trending_products['total_anterior']
        ) / trending_products['total_anterior'].replace(0, 1) * 100
        
        trending_products['crecimiento_cantidad'] = (
            trending_products['cantidad_reciente'] - trending_products['cantidad_anterior']
        ) / trending_products['cantidad_anterior'].replace(0, 1) * 100
        
        # Score de trending
        trending_products['trending_score'] = (
            trending_products['crecimiento_ventas'] * 0.6 +
            trending_products['crecimiento_cantidad'] * 0.4
        )
        
        # Obtener información de productos
        productos_pandas = productos_df.toPandas()
        
        # Mergear con información de productos
        trending_products = trending_products.merge(
            productos_pandas[['product_id', 'nombre', 'categoria', 'precio']], 
            on='product_id'
        )
        
        # Ordenar por trending score
        trending_products = trending_products.sort_values('trending_score', ascending=False).head(limit)
        
        # Detener Spark
        data_generator.stop_spark()
        
        # Convertir a formato de respuesta
        response = []
        for _, row in trending_products.iterrows():
            response.append({
                "product_id": row['product_id'],
                "nombre": row['nombre'],
                "categoria": row['categoria'],
                "precio": round(row['precio'], 2),
                "ventas_recientes": round(row['total_reciente'], 2),
                "ventas_anteriores": round(row['total_anterior'], 2),
                "crecimiento_ventas": round(row['crecimiento_ventas'], 2),
                "crecimiento_cantidad": round(row['crecimiento_cantidad'], 2),
                "trending_score": round(row['trending_score'], 2)
            })
        
        return {
            "productos_trending": response,
            "periodo_analisis": {
                "dias": days,
                "fecha_inicio": fecha_inicio.strftime('%Y-%m-%d'),
                "fecha_fin": fecha_max.strftime('%Y-%m-%d')
            },
            "total_productos": len(response)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo productos trending: {str(e)}")

