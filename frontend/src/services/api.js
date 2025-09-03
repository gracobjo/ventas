import axios from 'axios';

// Configurar axios
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000, // Aumentar timeout a 30 segundos
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    // Agregar timestamp para cache busting
    if (config.method === 'get') {
      config.params = { ...config.params, _t: Date.now() };
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Servicios de la API
export const apiService = {
  // Dashboard y resumen
  getSummary: () => api.get('/summary'),
  getMetrics: () => api.get('/summary/metrics'),
  getDashboardData: () => api.get('/summary/dashboard'),

  // Productos
  getTopProducts: (params = {}) => api.get('/products/top', { params }),
  getCategories: () => api.get('/products/categories'),
  getProductDetails: (productId) => api.get(`/products/${productId}`),
  getProductTrends: () => api.get('/products/performance/trends'),
  getInventoryAnalysis: () => api.get('/products/inventory/analysis'),

  // Clientes
  getCustomersRFM: (params = {}) => api.get('/customers/rfm', { params }),
  getCustomerSegments: () => api.get('/customers/segments'),
  getCustomerDetails: (customerId) => api.get(`/customers/${customerId}`),
  getCustomerBehavior: () => api.get('/customers/behavior/analysis'),
  getCustomerRetention: () => api.get('/customers/retention/analysis'),

  // Forecasting
  getForecast: (params = {}) => api.get('/forecast', { params }),
  getForecastComparison: () => api.get('/forecast/models/compare'),
  getForecastHistory: () => api.get('/forecast/history'),
  getSalesTrends: () => api.get('/forecast/trends'),
  postCustomForecast: (data) => api.post('/forecast/custom', data),

  // Recomendaciones
  getCustomerRecommendations: (customerId, params = {}) => 
    api.get(`/recommendations/${customerId}`, { params }),
  getSimilarProducts: (productId, params = {}) => 
    api.get(`/recommendations/products/${productId}/similar`, { params }),
  getRecommendationStats: () => api.get('/recommendations/system/stats'),
  getRecommendationEvaluation: () => api.get('/recommendations/evaluation'),
  getPopularRecommendations: (params = {}) => 
    api.get('/recommendations/popular', { params }),
  getTrendingRecommendations: (params = {}) => 
    api.get('/recommendations/trending', { params }),
};

// Utilidades para manejo de errores
export const handleApiError = (error) => {
  if (error.response) {
    // Error de respuesta del servidor
    const { status, data } = error.response;
    switch (status) {
      case 400:
        return `Error de validación: ${data.detail || 'Datos inválidos'}`;
      case 404:
        return 'Recurso no encontrado';
      case 500:
        return 'Error interno del servidor';
      default:
        return `Error ${status}: ${data.detail || 'Error desconocido'}`;
    }
  } else if (error.request) {
    // Error de red
    return 'Error de conexión. Verifica tu conexión a internet.';
  } else {
    // Otros errores
    return 'Error inesperado';
  }
};

// Utilidades para formateo de datos
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('es-ES', {
    style: 'currency',
    currency: 'EUR',
  }).format(amount);
};

export const formatNumber = (number) => {
  return new Intl.NumberFormat('es-ES').format(number);
};

export const formatPercentage = (value) => {
  return `${(value * 100).toFixed(2)}%`;
};

export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

export default apiService;

