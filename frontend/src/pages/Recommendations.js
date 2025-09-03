import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Users, Sparkles } from 'lucide-react';

const Recommendations = () => {
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Recomendaciones
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Sistema de recomendaciones inteligente
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
        >
          <div className="p-6 text-center">
            <Heart className="h-12 w-12 text-blue-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Colaborativo
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Basado en comportamiento de usuarios
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
        >
          <div className="p-6 text-center">
            <Users className="h-12 w-12 text-green-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Basado en Contenido
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Basado en características de productos
            </p>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
        >
          <div className="p-6 text-center">
            <Sparkles className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Híbrido
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Combinación de ambos enfoques
            </p>
          </div>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700"
      >
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Funcionalidades de Recomendaciones
          </h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Análisis Disponible:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Recomendaciones personalizadas
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Productos similares
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Productos populares
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Productos en tendencia
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                  Evaluación de precisión
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Próximamente:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
                  Recomendaciones en tiempo real
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
                  Análisis de sentimientos
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
                  Recomendaciones contextuales
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
                  A/B testing de modelos
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-gray-400 rounded-full mr-3"></span>
                  Optimización automática
                </li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Recommendations;

