import React from 'react';
import { useQuery } from 'react-query';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Users, 
  Package, 
  DollarSign, 
  BarChart3,
  Activity,
  Target,
  Zap
} from 'lucide-react';
import toast from 'react-hot-toast';

import { apiService, handleApiError, formatCurrency, formatNumber } from '../services/api';

const Dashboard = () => {
  // Obtener datos del dashboard
  const { data: summary, isLoading: summaryLoading, error: summaryError } = useQuery(
    'dashboard-summary',
    apiService.getSummary,
    {
      refetchInterval: 30000, // Refrescar cada 30 segundos
      staleTime: 60000, // Datos frescos por 1 minuto
    }
  );

  const { data: metrics, isLoading: metricsLoading } = useQuery(
    'dashboard-metrics',
    apiService.getMetrics,
    {
      refetchInterval: 30000,
      staleTime: 60000,
    }
  );

  // Manejar errores
  React.useEffect(() => {
    if (summaryError) {
      toast.error(handleApiError(summaryError));
    }
  }, [summaryError]);

  // Componente de tarjeta de métrica
  const MetricCard = ({ title, value, icon: Icon, color, change, loading }) => {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.1 }}
        className="card fade-in"
      >
        <div className="card-body">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-secondary">
                {title}
              </p>
              {loading ? (
                <div className="skeleton h-8 w-24 mt-2" />
              ) : (
                <p className="text-2xl font-bold text-primary mt-1">
                  {value}
                </p>
              )}
              {change && (
                <div className="flex items-center mt-2 gap-sm">
                  <TrendingUp className={`h-4 w-4 ${change > 0 ? 'text-success' : 'text-danger'}`} />
                  <span className={`text-sm font-medium ${change > 0 ? 'text-success' : 'text-danger'}`}>
                    {change > 0 ? '+' : ''}{change}%
                  </span>
                </div>
              )}
            </div>
            <div className={`p-3 rounded-full ${color} shadow-md`}>
              <Icon className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
      </motion.div>
    );
  };

  if (summaryLoading || metricsLoading) {
    return (
      <div className="container p-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-lg">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card">
              <div className="card-body">
                <div className="skeleton h-4 w-20 mb-md" />
                <div className="skeleton h-8 w-16" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container p-lg">
      {/* Header */}
      <div className="mb-xl">
        <h1 className="text-3xl font-bold text-primary mb-sm">
          Dashboard
        </h1>
        <p className="text-secondary text-lg">
          Resumen general del negocio e-commerce
        </p>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-lg mb-xl">
        <MetricCard
          title="Ventas Totales"
          value={summary ? formatCurrency(summary.total_ventas) : '€0'}
          icon={DollarSign}
          color="bg-primary"
          change={metrics?.crecimiento_mensual}
          loading={summaryLoading}
        />
        <MetricCard
          title="Clientes Activos"
          value={summary ? formatNumber(summary.num_clientes) : '0'}
          icon={Users}
          color="bg-success"
          loading={summaryLoading}
        />
        <MetricCard
          title="Productos Vendidos"
          value={summary ? formatNumber(summary.num_productos) : '0'}
          icon={Package}
          color="bg-warning"
          loading={summaryLoading}
        />
        <MetricCard
          title="Ticket Promedio"
          value={summary ? formatCurrency(summary.ticket_promedio) : '€0'}
          icon={BarChart3}
          color="bg-danger"
          loading={summaryLoading}
        />
      </div>

      {/* Gráficos y análisis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Ventas por mes */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Ventas Mensuales
            </h3>
          </div>
          <div className="card-body">
            {summary?.ventas_mensuales ? (
              <div className="space-y-3">
                {summary.ventas_mensuales.slice(-6).map((venta, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {venta.fecha}
                    </span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {formatCurrency(venta.ventas)}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                No hay datos disponibles
              </div>
            )}
          </div>
        </motion.div>

        {/* Top categorías */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Top Categorías
            </h3>
          </div>
          <div className="card-body">
            {summary?.top_categorias ? (
              <div className="space-y-3">
                {summary.top_categorias.map((categoria, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {categoria.categoria}
                    </span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      {formatCurrency(categoria.ventas)}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                No hay datos disponibles
              </div>
            )}
          </div>
        </motion.div>
      </div>

      {/* Insights rápidos */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Insights Rápidos
          </h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <Activity className="h-8 w-8 text-primary-500 mx-auto mb-2" />
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Margen Promedio
              </p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {summary ? `${summary.margen_porcentaje}%` : '0%'}
              </p>
            </div>
            <div className="text-center">
              <Target className="h-8 w-8 text-success-500 mx-auto mb-2" />
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Canal Principal
              </p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {summary?.canales_venta?.[0]?.canal || 'N/A'}
              </p>
            </div>
            <div className="text-center">
              <Zap className="h-8 w-8 text-warning-500 mx-auto mb-2" />
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Última Actualización
              </p>
              <p className="text-lg font-semibold text-gray-900 dark:text-white">
                {summary ? new Date(summary.ultima_actualizacion).toLocaleTimeString() : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;

