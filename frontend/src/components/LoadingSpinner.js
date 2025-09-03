import React from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ size = 'md', text = 'Cargando...', className = '' }) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12'
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={`flex flex-col items-center justify-center p-lg ${className}`}
    >
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        className={`text-primary ${sizeClasses[size]}`}
      >
        <Loader2 className="h-full w-full" />
      </motion.div>
      {text && (
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-secondary text-sm font-medium mt-md"
        >
          {text}
        </motion.p>
      )}
    </motion.div>
  );
};

// Componente de skeleton para contenido
export const Skeleton = ({ className = '', height = 'h-4', width = 'w-full' }) => {
  return (
    <div className={`skeleton ${height} ${width} ${className}`} />
  );
};

// Componente de skeleton para cards
export const SkeletonCard = ({ lines = 3 }) => {
  return (
    <div className="card">
      <div className="card-body">
        <div className="space-y-md">
          <Skeleton height="h-4" width="w-3/4" />
          <Skeleton height="h-6" width="w-1/2" />
          {lines > 2 && <Skeleton height="h-4" width="w-2/3" />}
        </div>
      </div>
    </div>
  );
};

// Componente de skeleton para métricas
export const SkeletonMetric = () => {
  return (
    <div className="card">
      <div className="card-body">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <Skeleton height="h-4" width="w-20" className="mb-sm" />
            <Skeleton height="h-8" width="w-16" />
          </div>
          <div className="skeleton h-12 w-12 rounded-full" />
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;

