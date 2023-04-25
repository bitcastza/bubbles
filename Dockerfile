FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -qq && apt-get upgrade -y -qq
RUN apt-get install -y -qq netcat-openbsd npm
RUN npm install --global yarn

WORKDIR /app

COPY requirements.txt ./

RUN pip3 install -U pip
RUN pip3 install uwsgi
RUN pip3 install --no-cache-dir -r requirements.txt

ADD package.json yarn.lock ./
RUN yarn install

COPY docker/uwsgi.ini /etc/uwsgi/bubbles.ini
COPY ./ /app

EXPOSE 8000
CMD /app/docker/docker-entrypoint.prod.sh
