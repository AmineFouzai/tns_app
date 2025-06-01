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

CMD ["sh", "-c", " python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate && python manage.py seed_merchants.py && python manage.py seed_recipients.py && python manage.py seed_templates.py && python manage.py seed_campaigns.py && python manage.py  test && gunicorn server.wsgi:application --bind 0.0.0.0:8000"]
