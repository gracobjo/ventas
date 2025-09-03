# Usar imagen base de Node.js
FROM node:18-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias (incluyendo devDependencies para el build)
RUN npm install

# Copiar código de la aplicación
COPY . .

# Construir la aplicación
RUN npm run build

# Usar nginx para servir la aplicación
FROM nginx:alpine

# Copiar la configuración de nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar los archivos construidos
COPY --from=0 /app/build /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Comando para ejecutar nginx
CMD ["nginx", "-g", "daemon off;"]

