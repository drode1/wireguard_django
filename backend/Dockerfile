FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install vim -y --no-install-recommends

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "wireguard_django.wsgi:application", "--bind", "0:8000" ]
