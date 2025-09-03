import React from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Calendar, BarChart3 } from 'lucide-react';

const Forecast = () => {
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Pronósticos
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Predicciones de ventas con IA
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="card"
        >
          <div className="card-body text-center">
            <TrendingUp className="h-12 w-12 text-primary-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Prophet
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Modelo de Facebook para series temporales
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="card-body text-center">
            <BarChart3 className="h-12 w-12 text-success-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              ARIMA
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Modelo estadístico tradicional
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="card-body text-center">
            <Calendar className="h-12 w-12 text-warning-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Comparación
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Evaluación de modelos
            </p>
          </div>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Funcionalidades de Pronósticos
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Análisis Disponible:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Predicciones mensuales</li>
                <li>• Comparación de modelos</li>
                <li>• Análisis de tendencias</li>
                <li>• Intervalos de confianza</li>
                <li>• Métricas de precisión</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Próximamente:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Predicciones por categoría</li>
                <li>• Análisis estacional</li>
                <li>• Alertas de anomalías</li>
                <li>• Optimización de inventario</li>
                <li>• Predicciones personalizadas</li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Forecast;

