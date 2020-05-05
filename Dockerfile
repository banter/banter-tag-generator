FROM python:3.6.3

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt --default-timeout=10000 --no-cache-dir -v

CMD python app.py
