FROM nginx:latest

USER root

RUN ln -snf /usr/share/zoneinfo/America/Fortaleza /etc/localtime && echo America/Fortaleza > /etc/timezone

COPY nginx.conf /etc/nginx/nginx.conf

VOLUME /var/log/nginx
