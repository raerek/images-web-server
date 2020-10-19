from python:3.9-alpine

COPY . /app

WORKDIR /app

RUN pip3 --no-cache-dir install -r requirements.txt

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]
