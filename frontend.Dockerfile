# Usamos el servidor web ultraligero
FROM nginx:alpine

# Borramos los archivos y la configuración por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*
RUN rm /etc/nginx/conf.d/default.conf

# Copiamos toda tu carpeta frontend
COPY ./frontend /usr/share/nginx/html

# Configuramos Nginx para entender tu estructura de carpetas
RUN echo 'server { \
    listen 80; \
    root /usr/share/nginx/html; \
    \
    # Si entran a la raíz (localhost), mostramos silenciosamente el index \
    location = / { \
        try_files /views/index.html =404; \
    } \
    \
    # Si piden scripts/styles los da normal, si piden un .html lo busca en /views \
    location / { \
        try_files $uri $uri/ /views$uri /views$uri/ =404; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Exponemos el puerto
EXPOSE 80

# Arrancamos Nginx
CMD ["nginx", "-g", "daemon off;"]