# ⚡ Guía de Arranque Rápido

## 🚀 Inicio en 5 Minutos

### 1. Verificar Prerrequisitos

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version
```

### 2. Clonar y Ejecutar

```bash
# Clonar el repositorio
git clone <repository-url>
cd ventas

# Ejecutar todo con un comando
docker-compose up -d
```

### 3. Verificar Funcionamiento

```bash
# Verificar contenedores
docker-compose ps

# Verificar backend
curl http://localhost:8000/health

# Verificar frontend
curl http://localhost:3000
```

### 4. Acceder a la Aplicación

- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- ⚡ **Spark UI**: http://localhost:8080

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f

# Reconstruir
docker-compose build --no-cache
docker-compose up -d
```

### Desarrollo

```bash
# Ejecutar solo backend
docker-compose up backend -d

# Ejecutar solo frontend
docker-compose up frontend -d

# Ver logs específicos
docker-compose logs backend
docker-compose logs frontend
```

### Troubleshooting

```bash
# Limpiar todo
docker-compose down --volumes --remove-orphans
docker system prune -a

# Reiniciar todo
docker-compose restart

# Verificar recursos
docker stats
```

## 📊 Datos de Ejemplo

La aplicación incluye datos sintéticos para demostración:

- **10,000+ productos** con categorías y precios
- **5,000+ clientes** con segmentación RFM
- **50,000+ transacciones** con fechas y cantidades
- **Modelos ML entrenados** para recomendaciones y forecasting

## 🎯 Funcionalidades Disponibles

### ✅ Implementadas

- [x] Dashboard con métricas en tiempo real
- [x] Gestión de productos y clientes
- [x] Sistema de recomendaciones
- [x] Forecasting de ventas
- [x] API REST completa
- [x] Interfaz responsive
- [x] Tema oscuro/claro

### 🚧 En Desarrollo

- [ ] Autenticación de usuarios
- [ ] Notificaciones en tiempo real
- [ ] Exportación de reportes
- [ ] Integración con bases de datos externas

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Crear archivo .env
cp env.example .env

# Editar configuración
nano .env
```

### Puertos Personalizados

Editar `docker-compose.yml`:

```yaml
ports:
  - "3001:80"  # Frontend en puerto 3001
  - "8001:8000"  # Backend en puerto 8001
```

### Recursos de Docker

- **Memoria**: Mínimo 4GB recomendado
- **CPU**: 2 cores mínimo
- **Disco**: 10GB espacio libre

## 📞 Soporte Rápido

### Problemas Comunes

1. **Docker no inicia**: Verificar que Docker Desktop esté ejecutándose
2. **Puertos ocupados**: Cambiar puertos en docker-compose.yml
3. **Memoria insuficiente**: Aumentar memoria en Docker Desktop
4. **Contenedores no se conectan**: Verificar red Docker

### Logs de Error

```bash
# Ver todos los logs
docker-compose logs

# Ver logs específicos
docker-compose logs backend --tail=50
docker-compose logs frontend --tail=50
```

### Reinicio Completo

```bash
# Parar todo
docker-compose down

# Limpiar
docker system prune -a

# Reconstruir
docker-compose build --no-cache

# Iniciar
docker-compose up -d
```

## 🎉 ¡Listo!

Una vez que veas todos los contenedores en estado "Up", la aplicación estará lista para usar.

**¡Disfruta explorando el sistema de análisis inteligente de e-commerce!** 🚀
