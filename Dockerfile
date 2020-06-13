FROM python:3.6.3

ADD . /src

WORKDIR /src

RUN pip install -r docker_or_local_req.txt --default-timeout=10000 --no-cache-dir -v

CMD waitress-serve --listen 0.0.0.0:5000 wsgi:app
