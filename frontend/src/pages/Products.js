import React from 'react';
import { motion } from 'framer-motion';
import { Package, TrendingUp, DollarSign } from 'lucide-react';

const Products = () => {
  return (
    <div className="p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Productos
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Análisis y gestión de productos
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="card"
        >
          <div className="card-body text-center">
            <Package className="h-12 w-12 text-primary-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Top Productos
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Productos más vendidos y rentables
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
            <TrendingUp className="h-12 w-12 text-success-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Análisis de Rendimiento
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Métricas y tendencias de productos
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
            <DollarSign className="h-12 w-12 text-warning-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Gestión de Inventario
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Control de stock y rotación
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
            Funcionalidades de Productos
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Análisis Disponible:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Top productos por ventas</li>
                <li>• Análisis por categorías</li>
                <li>• Rendimiento temporal</li>
                <li>• Gestión de inventario</li>
                <li>• Análisis de márgenes</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 dark:text-white mb-3">
                Próximamente:
              </h4>
              <ul className="space-y-2 text-gray-600 dark:text-gray-400">
                <li>• Predicción de demanda</li>
                <li>• Optimización de precios</li>
                <li>• Análisis de competencia</li>
                <li>• Alertas de stock</li>
                <li>• Recomendaciones de productos</li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Products;

