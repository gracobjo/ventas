"""
📈 Endpoint de Forecasting
Predicciones de ventas usando Prophet y ARIMA
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta

from app.utils.data_generator import DataGenerator
from app.ml.forecasting import SalesForecaster

router = APIRouter()

class ForecastResponse(BaseModel):
    """Respuesta del endpoint de forecasting"""
    predicciones: List[Dict]
    modelo_utilizado: str
    metricas_rendimiento: Optional[Dict]
    periodo_prediccion: Dict
    ultima_actualizacion: str

class ForecastRequest(BaseModel):
    """Request para forecasting personalizado"""
    periods: int = 6
    model_type: Optional[str] = "auto"  # auto, prophet, arima

@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    periods: int = Query(6, description="Número de períodos a predecir", ge=1, le=12),
    model_type: str = Query("auto", description="Tipo de modelo: auto, prophet, arima")
):
    """Obtiene predicciones de ventas futuras"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar forecaster
        forecaster = SalesForecaster()
        
        # Intentar cargar modelos existentes
        try:
            forecaster.load_models()
            print("✅ Modelos cargados desde archivo")
        except:
            print("🔄 Entrenando nuevos modelos...")
            # Preparar datos de series temporales
            time_series_data = forecaster.prepare_time_series_data(df_completo)
            
            # Entrenar y comparar modelos
            if model_type == "auto":
                results = forecaster.compare_models(time_series_data)
                forecaster.save_models()
            elif model_type == "prophet":
                forecaster.train_prophet_model(time_series_data)
                forecaster.best_model = "prophet"
                forecaster.save_models()
            elif model_type == "arima":
                forecaster.train_arima_model(time_series_data)
                forecaster.best_model = "arima"
                forecaster.save_models()
            else:
                raise ValueError("Tipo de modelo no válido")
        
        # Preparar datos para predicción
        time_series_data = forecaster.prepare_time_series_data(df_completo)
        
        # Obtener predicciones
        predicciones = forecaster.predict_future_sales(periods, time_series_data)
        
        # Obtener métricas de rendimiento
        metricas = forecaster.get_model_performance(time_series_data)
        
        # Calcular período de predicción
        ultima_fecha = time_series_data['ds'].max()
        fecha_inicio = ultima_fecha + timedelta(days=1)
        fecha_fin = fecha_inicio + timedelta(days=periods-1)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return ForecastResponse(
            predicciones=predicciones,
            modelo_utilizado=forecaster.best_model,
            metricas_rendimiento=metricas,
            periodo_prediccion={
                "inicio": fecha_inicio.strftime('%Y-%m-%d'),
                "fin": fecha_fin.strftime('%Y-%m-%d'),
                "periodos": periods
            },
            ultima_actualizacion=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en forecasting: {str(e)}")

@router.post("/forecast/custom", response_model=ForecastResponse)
async def custom_forecast(request: ForecastRequest):
    """Endpoint POST para forecasting personalizado"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar forecaster
        forecaster = SalesForecaster()
        
        # Cargar modelos existentes o entrenar nuevos
        try:
            forecaster.load_models()
        except:
            time_series_data = forecaster.prepare_time_series_data(df_completo)
            if request.model_type == "auto":
                forecaster.compare_models(time_series_data)
            elif request.model_type == "prophet":
                forecaster.train_prophet_model(time_series_data)
                forecaster.best_model = "prophet"
            elif request.model_type == "arima":
                forecaster.train_arima_model(time_series_data)
                forecaster.best_model = "arima"
            forecaster.save_models()
        
        # Preparar datos para predicción
        time_series_data = forecaster.prepare_time_series_data(df_completo)
        
        # Obtener predicciones
        predicciones = forecaster.predict_future_sales(request.periods, time_series_data)
        
        # Obtener métricas de rendimiento
        metricas = forecaster.get_model_performance(time_series_data)
        
        # Calcular período de predicción
        ultima_fecha = time_series_data['ds'].max()
        fecha_inicio = ultima_fecha + timedelta(days=1)
        fecha_fin = fecha_inicio + timedelta(days=request.periods-1)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return ForecastResponse(
            predicciones=predicciones,
            modelo_utilizado=forecaster.best_model,
            metricas_rendimiento=metricas,
            periodo_prediccion={
                "inicio": fecha_inicio.strftime('%Y-%m-%d'),
                "fin": fecha_fin.strftime('%Y-%m-%d'),
                "periodos": request.periods
            },
            ultima_actualizacion=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en forecasting personalizado: {str(e)}")

@router.get("/forecast/models/compare")
async def compare_forecast_models():
    """Compara el rendimiento de diferentes modelos de forecasting"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar forecaster
        forecaster = SalesForecaster()
        
        # Preparar datos
        time_series_data = forecaster.prepare_time_series_data(df_completo)
        
        # Comparar modelos
        results = forecaster.compare_models(time_series_data)
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "comparacion": {
                "prophet": {
                    "rmse": round(results['prophet']['rmse'], 2),
                    "mae": round(results['prophet']['mae'], 2)
                },
                "arima": {
                    "rmse": round(results['arima']['rmse'], 2),
                    "mae": round(results['arima']['mae'], 2)
                }
            },
            "mejor_modelo": results['best_model'],
            "datos_utilizados": {
                "periodos": len(time_series_data),
                "fecha_inicio": time_series_data['ds'].min().strftime('%Y-%m-%d'),
                "fecha_fin": time_series_data['ds'].max().strftime('%Y-%m-%d')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando modelos: {str(e)}")

@router.get("/forecast/history")
async def get_forecast_history():
    """Obtiene historial de predicciones vs valores reales"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        
        # Inicializar forecaster
        forecaster = SalesForecaster()
        
        # Preparar datos
        time_series_data = forecaster.prepare_time_series_data(df_completo)
        
        # Dividir datos para evaluación
        test_size = 30
        train_data = time_series_data.iloc[:-test_size]
        test_data = time_series_data.iloc[-test_size:]
        
        # Cargar o entrenar modelo
        try:
            forecaster.load_models()
        except:
            forecaster.compare_models(time_series_data)
        
        # Generar predicciones para el período de prueba
        if forecaster.best_model == "prophet":
            forecast = forecaster.prophet_model.predict(test_data[['ds']])
            predictions = forecast['yhat'].values
        else:
            if forecaster.arima_model:
                predictions = forecaster.arima_model.forecast(steps=test_size)
            else:
                predictions = [0] * test_size
        
        # Preparar datos de respuesta
        actual_values = test_data['y'].values
        dates = test_data['ds'].dt.strftime('%Y-%m-%d').values
        
        history_data = []
        for i, (date, actual, pred) in enumerate(zip(dates, actual_values, predictions)):
            history_data.append({
                "fecha": date,
                "valor_real": round(actual, 2),
                "prediccion": round(max(0, pred), 2),
                "error": round(abs(actual - pred), 2),
                "error_porcentual": round(abs(actual - pred) / actual * 100, 2) if actual > 0 else 0
            })
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "historial": history_data,
            "metricas": {
                "rmse": round(((actual_values - predictions) ** 2).mean() ** 0.5, 2),
                "mae": round(abs(actual_values - predictions).mean(), 2),
                "mape": round(abs(actual_values - predictions) / actual_values * 100, 2).mean()
            },
            "modelo_utilizado": forecaster.best_model,
            "periodo_evaluacion": {
                "inicio": dates[0],
                "fin": dates[-1],
                "dias": len(dates)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial: {str(e)}")

@router.get("/forecast/trends")
async def get_sales_trends():
    """Obtiene tendencias y patrones de ventas"""
    try:
        # Cargar datos
        data_generator = DataGenerator()
        productos_df, clientes_df, ventas_df = data_generator.load_data()
        
        # Obtener datos combinados
        df_completo = data_generator.get_combined_data()
        df_pandas = df_completo.toPandas()
        
        # Análisis de tendencias
        ventas_diarias = df_pandas.groupby('fecha').agg({
            'total': 'sum',
            'cantidad': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Tendencia general
        ventas_diarias['fecha_num'] = (ventas_diarias['fecha'] - ventas_diarias['fecha'].min()).dt.days
        correlation = ventas_diarias['fecha_num'].corr(ventas_diarias['total'])
        
        # Estacionalidad semanal
        ventas_diarias['dia_semana'] = ventas_diarias['fecha'].dt.dayofweek
        estacionalidad_semanal = ventas_diarias.groupby('dia_semana')['total'].mean()
        
        # Estacionalidad mensual
        ventas_diarias['mes'] = ventas_diarias['fecha'].dt.month
        estacionalidad_mensual = ventas_diarias.groupby('mes')['total'].mean()
        
        # Detener Spark
        data_generator.stop_spark()
        
        return {
            "tendencia_general": {
                "correlacion_tiempo": round(correlation, 3),
                "direccion": "creciente" if correlation > 0 else "decreciente" if correlation < 0 else "estable"
            },
            "estacionalidad_semanal": [
                {
                    "dia": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][i],
                    "ventas_promedio": round(val, 2)
                }
                for i, val in estacionalidad_semanal.items()
            ],
            "estacionalidad_mensual": [
                {
                    "mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                           "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"][i-1],
                    "ventas_promedio": round(val, 2)
                }
                for i, val in estacionalidad_mensual.items()
            ],
            "patrones": {
                "mejor_dia": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][estacionalidad_semanal.idxmax()],
                "peor_dia": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][estacionalidad_semanal.idxmin()],
                "mejor_mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                             "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"][estacionalidad_mensual.idxmax()-1],
                "peor_mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", 
                            "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"][estacionalidad_mensual.idxmin()-1]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando tendencias: {str(e)}")

