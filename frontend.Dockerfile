# Usamos el servidor web ultraligero
FROM nginx:alpine

# Borramos los archivos y la configuración por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/* && rm /etc/nginx/conf.d/default.conf

# Copiamos tu archivo de configuración maestro (con Proxy Inverso + Optimizaciones)
COPY nginx-optimization.conf /etc/nginx/conf.d/default.conf

# Copiamos toda tu carpeta frontend al directorio del servidor
COPY ./frontend /usr/share/nginx/html

# Exponemos el puerto estándar web
EXPOSE 80

# Arrancamos Nginx
CMD ["nginx", "-g", "daemon off;"]