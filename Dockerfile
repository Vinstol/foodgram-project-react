FROM python:3.9
LABEL author='vinstol@yandex.ru' version=2021.11

WORKDIR /code
COPY requirements.txt /code
RUN python3 -m pip install --upgrade pip \
    && pip3 install -r /code/requirements.txt --no-cache-dir
COPY . /code
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000