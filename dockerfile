FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Entrypoint runs migrations, loads data, tests, and launches server
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata seed_data.json && pytest && gunicorn server.wsgi:application --bind 0.0.0.0:8000"]
