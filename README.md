# 🚀 E-Commerce AI Analytics

Sistema de análisis inteligente para e-commerce con capacidades de machine learning, forecasting y recomendaciones personalizadas.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [API Endpoints](#-api-endpoints)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)

## ✨ Características

### 🎯 Funcionalidades Principales

#### 📊 Dashboard Analytics
- **Métricas en Tiempo Real**: Ventas totales, clientes activos, productos vendidos, ticket promedio
- **Gráficos Interactivos**: Visualización de tendencias de ventas y crecimiento
- **KPIs Clave**: Indicadores de rendimiento del negocio
- **Resumen Ejecutivo**: Vista general del estado del e-commerce

#### 🛍️ Gestión de Productos
- **Catálogo Inteligente**: Gestión completa de productos con categorización automática
- **Análisis de Rendimiento**: Productos más vendidos, rentabilidad, stock
- **Optimización de Precios**: Recomendaciones de precios basadas en ML
- **Gestión de Inventario**: Alertas de stock bajo y predicciones de demanda

#### 👥 Gestión de Clientes
- **Segmentación Avanzada**: Clasificación automática de clientes por comportamiento
- **Análisis de Comportamiento**: Patrones de compra y preferencias
- **Lifetime Value**: Cálculo del valor de vida del cliente
- **Retención y Engagement**: Métricas de fidelización

#### 🔮 Forecasting & Predicciones
- **Predicción de Ventas**: Modelos de series temporales para forecasting
- **Análisis Estacional**: Patrones estacionales y tendencias
- **Demanda Futura**: Predicciones de demanda por producto
- **Optimización de Stock**: Recomendaciones de inventario

#### 🧠 Sistema de Recomendaciones
- **Recomendaciones Colaborativas**: Basadas en comportamiento de usuarios
- **Recomendaciones de Contenido**: Basadas en características de productos
- **Sistema Híbrido**: Combinación de ambos enfoques
- **Personalización**: Recomendaciones adaptadas a cada usuario

### 🛠️ Tecnologías Utilizadas

#### Backend
- **FastAPI**: Framework web moderno y rápido
- **PySpark**: Procesamiento de datos distribuido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Scikit-learn**: Machine Learning
- **Prophet**: Forecasting de series temporales
- **Implicit**: Sistema de recomendaciones

#### Frontend
- **React**: Framework de interfaz de usuario
- **Tailwind CSS**: Framework de estilos
- **Framer Motion**: Animaciones fluidas
- **React Query**: Gestión de estado del servidor
- **React Router**: Navegación SPA
- **Lucide React**: Iconografía moderna

#### Infraestructura
- **Docker**: Containerización
- **Docker Compose**: Orquestación de servicios
- **Nginx**: Servidor web y proxy reverso
- **Apache Spark**: Procesamiento distribuido

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Apache Spark  │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (ML Engine)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8080    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   SQLite DB     │    │   Data Storage  │
│   (Load Bal.)   │    │   (Local)       │    │   (CSV/JSON)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Instalación

### Prerrequisitos

- **Docker Desktop** instalado y ejecutándose
- **Git** para clonar el repositorio
- Mínimo **4GB RAM** disponible
- **Windows 10/11**, **macOS** o **Linux**

### Pasos de Instalación

#### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd ventas
```

#### 2. Configurar Variables de Entorno (Opcional)

```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar las variables según necesites
nano .env
```

#### 3. Construir y Ejecutar con Docker

```bash
# Construir todas las imágenes
docker-compose build

# Ejecutar todos los servicios
docker-compose up -d

# Verificar el estado de los contenedores
docker-compose ps
```

#### 4. Verificar la Instalación

```bash
# Verificar que el backend esté funcionando
curl http://localhost:8000/health

# Verificar que el frontend esté funcionando
curl http://localhost:3000
```

### Acceso a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Spark UI**: http://localhost:8080

## 📖 Uso

### Primeros Pasos

1. **Acceder al Dashboard**: Navega a http://localhost:3000
2. **Explorar las Secciones**: Usa el sidebar para navegar entre módulos
3. **Ver Datos de Ejemplo**: La aplicación incluye datos sintéticos para demostración
4. **Probar Funcionalidades**: Experimenta con las diferentes herramientas de análisis

### Navegación

- **Dashboard**: Vista general y métricas principales
- **Productos**: Gestión y análisis de productos
- **Clientes**: Segmentación y análisis de clientes
- **Forecasting**: Predicciones y análisis temporal
- **Recomendaciones**: Sistema de recomendaciones inteligente

### Funcionalidades Clave

#### Dashboard
- Métricas en tiempo real
- Gráficos interactivos
- KPIs del negocio
- Resumen ejecutivo

#### Productos
- Catálogo de productos
- Análisis de rendimiento
- Gestión de inventario
- Optimización de precios

#### Clientes
- Segmentación automática
- Análisis de comportamiento
- Lifetime value
- Métricas de retención

#### Forecasting
- Predicción de ventas
- Análisis estacional
- Demanda futura
- Optimización de stock

#### Recomendaciones
- Recomendaciones personalizadas
- Productos similares
- Productos populares
- Evaluación de precisión

## 🔌 API Endpoints

### Endpoints Principales

#### Health Check
```http
GET /health
```

#### Dashboard
```http
GET /api/v1/dashboard/summary
GET /api/v1/dashboard/metrics
```

#### Productos
```http
GET /api/v1/products
GET /api/v1/products/{product_id}
POST /api/v1/products
PUT /api/v1/products/{product_id}
DELETE /api/v1/products/{product_id}
```

#### Clientes
```http
GET /api/v1/customers
GET /api/v1/customers/{customer_id}
POST /api/v1/customers
PUT /api/v1/customers/{customer_id}
DELETE /api/v1/customers/{customer_id}
```

#### Forecasting
```http
GET /api/v1/forecast/sales
GET /api/v1/forecast/demand
POST /api/v1/forecast/generate
```

#### Recomendaciones
```http
GET /api/v1/recommendations/{user_id}
GET /api/v1/recommendations/similar/{product_id}
GET /api/v1/recommendations/popular
```

### Ejemplo de Uso de la API

```bash
# Obtener resumen del dashboard
curl http://localhost:8000/api/v1/dashboard/summary

# Obtener productos
curl http://localhost:8000/api/v1/products

# Obtener recomendaciones para un usuario
curl http://localhost:8000/api/v1/recommendations/user123
```

## 🗺️ Roadmap

### Fase 1: Mejoras Inmediatas (1-2 meses)

#### 🎨 UX/UI Improvements
- [ ] **Tema Oscuro Completo**: Implementación completa del modo oscuro
- [ ] **Responsive Design**: Optimización para dispositivos móviles
- [ ] **Animaciones Avanzadas**: Transiciones más fluidas y atractivas
- [ ] **Dashboard Personalizable**: Widgets configurables por usuario
- [ ] **Notificaciones en Tiempo Real**: Sistema de alertas push

#### 🔧 Funcionalidades Técnicas
- [ ] **Autenticación JWT**: Sistema de login y autorización
- [ ] **Caché Redis**: Mejora de rendimiento con caché
- [ ] **Logging Avanzado**: Sistema de logs estructurados
- [ ] **Monitoreo**: Métricas de aplicación y alertas
- [ ] **Tests Automatizados**: Suite completa de tests

#### 📊 Analytics Avanzados
- [ ] **Funnel Analysis**: Análisis de conversión de usuarios
- [ ] **Cohort Analysis**: Análisis de cohortes de clientes
- [ ] **A/B Testing**: Framework para testing de hipótesis
- [ ] **Heatmaps**: Visualización de comportamiento de usuarios
- [ ] **Real-time Analytics**: Métricas en tiempo real

### Fase 2: Expansión de ML (3-4 meses)

#### 🤖 Machine Learning Avanzado
- [ ] **Deep Learning**: Modelos de redes neuronales
- [ ] **NLP para Reviews**: Análisis de sentimientos de reviews
- [ ] **Computer Vision**: Análisis de imágenes de productos
- [ ] **AutoML**: Automatización de selección de modelos
- [ ] **MLOps Pipeline**: Pipeline completo de ML

#### 📈 Forecasting Mejorado
- [ ] **Multi-variable Forecasting**: Múltiples variables predictivas
- [ ] **Ensemble Methods**: Combinación de múltiples modelos
- [ ] **Uncertainty Quantification**: Intervalos de confianza
- [ ] **Scenario Planning**: Planificación de escenarios
- [ ] **Real-time Forecasting**: Predicciones en tiempo real

#### 🧠 Recomendaciones Avanzadas
- [ ] **Contextual Recommendations**: Recomendaciones basadas en contexto
- [ ] **Multi-objective Optimization**: Optimización de múltiples objetivos
- [ ] **Cold Start Solutions**: Soluciones para nuevos usuarios/productos
- [ ] **Explainable AI**: Explicación de recomendaciones
- [ ] **Bandit Algorithms**: Algoritmos de bandit para optimización

### Fase 3: Escalabilidad (5-6 meses)

#### 🏗️ Arquitectura Distribuida
- [ ] **Microservicios**: Descomposición en microservicios
- [ ] **Message Queues**: Sistema de colas asíncronas
- [ ] **Event Streaming**: Procesamiento de eventos en tiempo real
- [ ] **Service Mesh**: Gestión de comunicación entre servicios
- [ ] **API Gateway**: Gateway centralizado para APIs

#### ☁️ Cloud Deployment
- [ ] **Kubernetes**: Orquestación de contenedores
- [ ] **Multi-cloud**: Soporte para múltiples nubes
- [ ] **Auto-scaling**: Escalado automático basado en demanda
- [ ] **CDN Integration**: Red de distribución de contenido
- [ ] **Backup & Recovery**: Sistema de respaldo y recuperación

#### 🔐 Seguridad Avanzada
- [ ] **OAuth 2.0**: Autenticación OAuth completa
- [ ] **RBAC**: Control de acceso basado en roles
- [ ] **Data Encryption**: Encriptación de datos en reposo y tránsito
- [ ] **Audit Logging**: Registro de auditoría completo
- [ ] **Compliance**: Cumplimiento de regulaciones (GDPR, CCPA)

### Fase 4: Innovación (7-8 meses)

#### 🚀 Funcionalidades Avanzadas
- [ ] **Voice Interface**: Interfaz de voz para consultas
- [ ] **AR/VR Integration**: Integración con realidad aumentada
- [ ] **IoT Integration**: Integración con dispositivos IoT
- [ ] **Blockchain**: Transacciones seguras con blockchain
- [ ] **Edge Computing**: Procesamiento en el edge

#### 📱 Mobile App
- [ ] **React Native App**: Aplicación móvil nativa
- [ ] **Offline Capabilities**: Funcionalidades offline
- [ ] **Push Notifications**: Notificaciones push avanzadas
- [ ] **Biometric Auth**: Autenticación biométrica
- [ ] **Mobile Analytics**: Analytics específicos para móvil

#### 🔮 AI Avanzado
- [ ] **Generative AI**: Generación de contenido con IA
- [ ] **Conversational AI**: Chatbots inteligentes
- [ ] **Predictive Maintenance**: Mantenimiento predictivo
- [ ] **Anomaly Detection**: Detección de anomalías
- [ ] **Auto-optimization**: Optimización automática de procesos

### Fase 5: Enterprise (9-12 meses)

#### 🏢 Funcionalidades Enterprise
- [ ] **Multi-tenancy**: Soporte multi-tenant
- [ ] **SSO Integration**: Integración con SSO empresarial
- [ ] **Custom Branding**: Personalización de marca
- [ ] **White-label Solution**: Solución white-label
- [ ] **API Marketplace**: Marketplace de APIs

#### 📊 Business Intelligence
- [ ] **Advanced Reporting**: Reportes avanzados
- [ ] **Data Warehousing**: Almacén de datos
- [ ] **ETL Pipelines**: Pipelines de extracción, transformación y carga
- [ ] **Data Governance**: Gobierno de datos
- [ ] **Compliance Reporting**: Reportes de cumplimiento

#### 🌐 Integración Global
- [ ] **Multi-language**: Soporte multiidioma
- [ ] **Multi-currency**: Soporte multicurrency
- [ ] **Localization**: Localización completa
- [ ] **Global CDN**: CDN global
- [ ] **Regional Compliance**: Cumplimiento regional

## 🔧 Troubleshooting

### Problemas Comunes

#### Docker no inicia
```bash
# Verificar que Docker Desktop esté ejecutándose
docker --version

# Reiniciar Docker Desktop si es necesario
```

#### Contenedores no se inician
```bash
# Verificar logs
docker-compose logs

# Limpiar contenedores
docker-compose down --volumes --remove-orphans

# Reconstruir
docker-compose build --no-cache
docker-compose up -d
```

#### Problemas de puertos
```bash
# Verificar puertos en uso
netstat -an | findstr :3000
netstat -an | findstr :8000

# Cambiar puertos en docker-compose.yml si es necesario
```

#### Problemas de memoria
```bash
# Aumentar memoria de Docker Desktop
# En Docker Desktop > Settings > Resources > Memory: 4GB+
```

#### Problemas de red
```bash
# Verificar conectividad
docker-compose exec backend ping frontend
docker-compose exec frontend ping backend
```

### Logs Útiles

```bash
# Logs del backend
docker-compose logs backend

# Logs del frontend
docker-compose logs frontend

# Logs de Spark
docker-compose logs spark-master
docker-compose logs spark-worker

# Logs en tiempo real
docker-compose logs -f
```

### Comandos Útiles

```bash
# Verificar estado de contenedores
docker-compose ps

# Reiniciar un servicio específico
docker-compose restart backend

# Ejecutar comandos dentro de contenedores
docker-compose exec backend python -c "print('Hello World')"

# Verificar uso de recursos
docker stats

# Limpiar recursos no utilizados
docker system prune -a
```

## 📞 Soporte

### Recursos Adicionales

- **Documentación API**: http://localhost:8000/docs
- **Spark UI**: http://localhost:8080
- **Issues**: Crear issue en el repositorio
- **Wiki**: Documentación adicional en el wiki del proyecto

### Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

### Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para el análisis inteligente de e-commerce**

