FROM nginx:1.23-alpine
COPY /etc/ssl/certs/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY /etc/ssl/private/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
