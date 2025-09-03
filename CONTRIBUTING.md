# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto E-Commerce AI Analytics! 

## 📋 Cómo Contribuir

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/TU_USUARIO/ventas.git
cd ventas
```

### 2. Configurar el Entorno

```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend
cd ../frontend
npm install
```

### 3. Crear una Rama

```bash
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/nombre-del-bug
```

### 4. Desarrollar

- Escribe código limpio y bien documentado
- Sigue las convenciones de estilo del proyecto
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario

### 5. Commit y Push

```bash
git add .
git commit -m "feat: añadir nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

### 6. Crear Pull Request

- Ve a tu fork en GitHub
- Crea un Pull Request hacia la rama `main`
- Describe claramente los cambios realizados

## 🎯 Áreas de Contribución

### Frontend (React)
- Nuevos componentes UI
- Mejoras en la experiencia de usuario
- Optimización de rendimiento
- Tests de componentes

### Backend (FastAPI)
- Nuevos endpoints API
- Mejoras en modelos de ML
- Optimización de consultas
- Tests de integración

### Machine Learning
- Nuevos algoritmos de recomendación
- Mejoras en modelos de forecasting
- Análisis de datos
- Optimización de rendimiento

### DevOps
- Mejoras en Docker
- Configuración de CI/CD
- Monitoreo y logging
- Seguridad

### Documentación
- Mejoras en README
- Documentación de API
- Guías de usuario
- Ejemplos de uso

## 📝 Convenciones

### Commits
Usa el formato [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: añadir nueva funcionalidad
fix: corregir bug en login
docs: actualizar README
style: formatear código
refactor: refactorizar componente
test: añadir tests
chore: actualizar dependencias
```

### Código
- **Python**: PEP 8, docstrings, type hints
- **JavaScript**: ESLint, Prettier, JSDoc
- **CSS**: Tailwind CSS, responsive design

### Tests
- Mantén cobertura de código > 80%
- Tests unitarios para nuevas funcionalidades
- Tests de integración para APIs
- Tests E2E para flujos críticos

## 🚀 Proceso de Review

1. **Code Review**: Todos los PRs requieren review
2. **Tests**: Deben pasar todos los tests
3. **Documentación**: Actualizar docs según sea necesario
4. **Merge**: Solo después de approval

## 🐛 Reportar Bugs

### Antes de reportar
- Busca en issues existentes
- Verifica que no sea un problema de configuración
- Reproduce el bug en un entorno limpio

### Template de Bug Report
```markdown
**Descripción del Bug**
Descripción clara y concisa del bug.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Ver error

**Comportamiento Esperado**
Lo que debería pasar.

**Comportamiento Actual**
Lo que realmente pasa.

**Screenshots**
Si aplica, añadir screenshots.

**Entorno**
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 90]
- Versión: [e.g. 1.0.0]

**Información Adicional**
Cualquier otra información relevante.
```

## 💡 Solicitar Features

### Template de Feature Request
```markdown
**Problema que resuelve**
Descripción del problema que esta feature resolvería.

**Solución propuesta**
Descripción de la solución que propones.

**Alternativas consideradas**
Otras soluciones que consideraste.

**Información adicional**
Cualquier otra información relevante.
```

## 📞 Contacto

- **Issues**: [GitHub Issues](https://github.com/gracobjo/ventas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/gracobjo/ventas/discussions)
- **Email**: [tu-email@ejemplo.com]

## 🎉 Reconocimiento

- Los contribuidores serán mencionados en el README
- Contribuciones significativas obtendrán acceso de mantenedor
- Badges especiales para contribuidores activos

---

**¡Gracias por hacer este proyecto mejor!** 🚀
