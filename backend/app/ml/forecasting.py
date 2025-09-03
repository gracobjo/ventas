"""
📈 Módulo de Forecasting Temporal
Implementa Prophet y ARIMA para predicciones de ventas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
import joblib
import os

warnings.filterwarnings('ignore')

class SalesForecaster:
    """Sistema de predicción de ventas usando Prophet y ARIMA"""
    
    def __init__(self):
        self.prophet_model = None
        self.arima_model = None
        self.best_model = None
        self.models_dir = "app/models"
        
        # Crear directorio de modelos si no existe
        os.makedirs(self.models_dir, exist_ok=True)
    
    def prepare_time_series_data(self, df_spark):
        """Prepara datos de series temporales desde Spark DataFrame"""
        print("📊 Preparando datos de series temporales...")
        
        # Convertir a pandas para análisis temporal
        df_pandas = df_spark.toPandas()
        
        # Agregar ventas por día
        daily_sales = df_pandas.groupby('fecha').agg({
            'total': 'sum',
            'cantidad': 'sum',
            'venta_id': 'count'
        }).reset_index()
        
        # Renombrar columnas para Prophet
        daily_sales = daily_sales.rename(columns={
            'fecha': 'ds',
            'total': 'y'
        })
        
        # Rellenar fechas faltantes con 0
        date_range = pd.date_range(
            start=daily_sales['ds'].min(),
            end=daily_sales['ds'].max(),
            freq='D'
        )
        
        complete_df = pd.DataFrame({'ds': date_range})
        daily_sales = complete_df.merge(daily_sales, on='ds', how='left').fillna(0)
        
        print(f"✅ Datos preparados: {len(daily_sales)} días")
        return daily_sales
    
    def train_prophet_model(self, data):
        """Entrena modelo Prophet"""
        print("🤖 Entrenando modelo Prophet...")
        
        # Configurar modelo Prophet
        self.prophet_model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10.0
        )
        
        # Agregar regresores si están disponibles
        if 'cantidad' in data.columns:
            self.prophet_model.add_regressor('cantidad')
        
        # Entrenar modelo
        self.prophet_model.fit(data)
        
        print("✅ Modelo Prophet entrenado")
        return self.prophet_model
    
    def train_arima_model(self, data):
        """Entrena modelo ARIMA"""
        print("📈 Entrenando modelo ARIMA...")
        
        # Preparar datos para ARIMA
        ts_data = data.set_index('ds')['y']
        
        # Verificar estacionariedad
        adf_result = adfuller(ts_data)
        is_stationary = adf_result[1] < 0.05
        
        if not is_stationary:
            # Diferenciar para hacer estacionario
            ts_data = ts_data.diff().dropna()
            print("  Datos diferenciados para estacionariedad")
        
        # Determinar parámetros ARIMA usando auto_arima o heurística
        # Para simplificar, usamos parámetros comunes
        try:
            self.arima_model = ARIMA(ts_data, order=(1, 1, 1)).fit()
            print("✅ Modelo ARIMA entrenado")
        except Exception as e:
            print(f"⚠️ Error entrenando ARIMA: {e}")
            # Fallback a parámetros más simples
            try:
                self.arima_model = ARIMA(ts_data, order=(0, 1, 1)).fit()
                print("✅ Modelo ARIMA entrenado (parámetros simplificados)")
            except:
                print("❌ No se pudo entrenar modelo ARIMA")
                self.arima_model = None
        
        return self.arima_model
    
    def compare_models(self, data, test_size=30):
        """Compara modelos Prophet vs ARIMA"""
        print("🔍 Comparando modelos...")
        
        # Dividir datos en train/test
        train_data = data.iloc[:-test_size]
        test_data = data.iloc[-test_size:]
        
        # Entrenar modelos
        prophet_model = self.train_prophet_model(train_data)
        arima_model = self.train_arima_model(train_data)
        
        # Predicciones Prophet
        prophet_forecast = prophet_model.predict(test_data[['ds']])
        prophet_predictions = prophet_forecast['yhat'].values
        
        # Predicciones ARIMA
        if arima_model:
            arima_predictions = arima_model.forecast(steps=test_size)
        else:
            arima_predictions = np.zeros(test_size)
        
        # Métricas de evaluación
        actual_values = test_data['y'].values
        
        prophet_rmse = np.sqrt(mean_squared_error(actual_values, prophet_predictions))
        prophet_mae = mean_absolute_error(actual_values, prophet_predictions)
        
        if arima_model:
            arima_rmse = np.sqrt(mean_squared_error(actual_values, arima_predictions))
            arima_mae = mean_absolute_error(actual_values, arima_predictions)
        else:
            arima_rmse = float('inf')
            arima_mae = float('inf')
        
        # Seleccionar mejor modelo
        if prophet_rmse < arima_rmse:
            self.best_model = 'prophet'
            print(f"🏆 Mejor modelo: Prophet (RMSE: {prophet_rmse:.2f})")
        else:
            self.best_model = 'arima'
            print(f"🏆 Mejor modelo: ARIMA (RMSE: {arima_rmse:.2f})")
        
        results = {
            'prophet': {
                'rmse': prophet_rmse,
                'mae': prophet_mae,
                'model': prophet_model
            },
            'arima': {
                'rmse': arima_rmse,
                'mae': arima_mae,
                'model': arima_model
            },
            'best_model': self.best_model
        }
        
        return results
    
    def predict_future_sales(self, periods=6, data=None):
        """Predice ventas futuras usando el mejor modelo"""
        if not self.best_model:
            raise ValueError("No hay modelo entrenado. Ejecuta compare_models() primero.")
        
        print(f"🔮 Prediciendo {periods} períodos futuros...")
        
        if self.best_model == 'prophet':
            return self._prophet_forecast(periods, data)
        else:
            return self._arima_forecast(periods, data)
    
    def _prophet_forecast(self, periods, data):
        """Predicción usando Prophet"""
        # Crear fechas futuras
        last_date = data['ds'].max()
        future_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=periods,
            freq='D'
        )
        
        future_df = pd.DataFrame({'ds': future_dates})
        
        # Agregar regresores si es necesario
        if 'cantidad' in data.columns:
            # Usar promedio de cantidad para predicciones futuras
            avg_cantidad = data['cantidad'].mean()
            future_df['cantidad'] = avg_cantidad
        
        # Predicción
        forecast = self.prophet_model.predict(future_df)
        
        # Preparar resultados
        results = []
        for i, row in forecast.iterrows():
            results.append({
                'fecha': row['ds'].strftime('%Y-%m-%d'),
                'prediccion': max(0, row['yhat']),
                'limite_inferior': max(0, row['yhat_lower']),
                'limite_superior': max(0, row['yhat_upper']),
                'modelo': 'Prophet'
            })
        
        return results
    
    def _arima_forecast(self, periods, data):
        """Predicción usando ARIMA"""
        if not self.arima_model:
            raise ValueError("Modelo ARIMA no disponible")
        
        # Predicción
        forecast = self.arima_model.forecast(steps=periods)
        
        # Preparar resultados
        results = []
        last_date = data['ds'].max()
        
        for i, pred in enumerate(forecast):
            fecha = last_date + timedelta(days=i+1)
            results.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'prediccion': max(0, pred),
                'limite_inferior': max(0, pred * 0.8),  # Aproximación
                'limite_superior': max(0, pred * 1.2),  # Aproximación
                'modelo': 'ARIMA'
            })
        
        return results
    
    def save_models(self):
        """Guarda los modelos entrenados"""
        print("💾 Guardando modelos...")
        
        if self.prophet_model:
            joblib.dump(self.prophet_model, f"{self.models_dir}/prophet_model.pkl")
        
        if self.arima_model:
            joblib.dump(self.arima_model, f"{self.models_dir}/arima_model.pkl")
        
        # Guardar información del mejor modelo
        model_info = {
            'best_model': self.best_model,
            'timestamp': datetime.now().isoformat()
        }
        joblib.dump(model_info, f"{self.models_dir}/model_info.pkl")
        
        print("✅ Modelos guardados")
    
    def load_models(self):
        """Carga modelos guardados"""
        print("📂 Cargando modelos...")
        
        try:
            self.prophet_model = joblib.load(f"{self.models_dir}/prophet_model.pkl")
            print("✅ Modelo Prophet cargado")
        except:
            print("⚠️ No se pudo cargar modelo Prophet")
        
        try:
            self.arima_model = joblib.load(f"{self.models_dir}/arima_model.pkl")
            print("✅ Modelo ARIMA cargado")
        except:
            print("⚠️ No se pudo cargar modelo ARIMA")
        
        try:
            model_info = joblib.load(f"{self.models_dir}/model_info.pkl")
            self.best_model = model_info['best_model']
            print(f"✅ Mejor modelo: {self.best_model}")
        except:
            print("⚠️ No se pudo cargar información del modelo")
    
    def get_model_performance(self, data, test_size=30):
        """Obtiene métricas de rendimiento del modelo"""
        if not self.best_model:
            return None
        
        # Dividir datos
        train_data = data.iloc[:-test_size]
        test_data = data.iloc[-test_size:]
        
        if self.best_model == 'prophet':
            # Predicción Prophet
            forecast = self.prophet_model.predict(test_data[['ds']])
            predictions = forecast['yhat'].values
        else:
            # Predicción ARIMA
            if self.arima_model:
                predictions = self.arima_model.forecast(steps=test_size)
            else:
                return None
        
        actual_values = test_data['y'].values
        
        # Calcular métricas
        rmse = np.sqrt(mean_squared_error(actual_values, predictions))
        mae = mean_absolute_error(actual_values, predictions)
        mape = np.mean(np.abs((actual_values - predictions) / actual_values)) * 100
        
        return {
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'model': self.best_model
        }

