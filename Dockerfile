FROM ubuntu:20.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    daphne \
    gunicorn \
    python3.8 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    nginx \
    supervisor \
    sqlite3 \
    openssl && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip setuptools
RUN pip3 install gevent

ADD . /project/

RUN pip3 install -r /project/requirements.txt
#RUN pip3 install /project/ljarrahd_app

RUN python3 /project/manage.py makemigrations
RUN python3 /project/manage.py migrate
RUN python3 /project/manage.py collectstatic --noinput

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
	-subj "/C=ru/ST=Kazan/L=Kazan/O=no/OU=no/CN=ljarrahd/" \
	-keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ljarrahd.com /etc/nginx/sites-available/ljarrahd.com
RUN ln -s /etc/nginx/sites-available/ljarrahd.com /etc/nginx/sites-enabled/; \
rm /etc/nginx/sites-available/default; \
rm /etc/nginx/sites-enabled/default;

RUN mkdir /run/daphne/
COPY supervisor-app-staging.conf /etc/supervisor/conf.d/
ENV DJANGO_SETTINGS_MODULE=rush01.settings

EXPOSE 80
#EXPOSE 443

CMD ["supervisord", "-n"]
