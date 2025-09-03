import React from 'react';
import { motion } from 'framer-motion';
import { Users, UserCheck, Target } from 'lucide-react';

const Customers = () => {
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Clientes
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Análisis RFM y segmentación de clientes
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="card"
        >
          <div className="card-body text-center">
            <Users className="h-12 w-12 text-primary-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Análisis RFM
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Recency, Frequency, Monetary
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
            <UserCheck className="h-12 w-12 text-success-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Segmentación
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Clasificación de clientes
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
            <Target className="h-12 w-12 text-warning-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Comportamiento
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Análisis de patrones de compra
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
            Funcionalidades de Clientes
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Análisis Disponible:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Análisis RFM completo</li>
                <li>• Segmentación de clientes</li>
                <li>• Análisis de retención</li>
                <li>• Comportamiento de compra</li>
                <li>• Valor del cliente (CLV)</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Próximamente:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Predicción de churn</li>
                <li>• Análisis de cohortes</li>
                <li>• Personalización avanzada</li>
                <li>• Campañas dirigidas</li>
                <li>• Análisis de satisfacción</li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Customers;

