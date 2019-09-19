FROM python:3

RUN apt-get update
RUN apt-get install -y -qq nginx

RUN rm /etc/nginx/sites-enabled/default

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install uwsgi
RUN pip3 install --no-cache-dir -r requirements.txt

COPY docker/uwsgi.ini /etc/uwsgi/bubbles.ini
COPY docker/nginx.conf /etc/nginx/sites-enabled/bubbles.conf
COPY scripts/start.sh /start.sh

COPY --chown=www-data:www-data . .

RUN python manage.py migrate

EXPOSE 80
CMD ["/start.sh"]
