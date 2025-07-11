FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .
COPY utils/ ./utils/

CMD ["waitress-serve", "--listen=0.0.0.0:8000", "app:app"]