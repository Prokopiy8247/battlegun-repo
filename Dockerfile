# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Create directory for static files
RUN mkdir -p /app/staticfiles && mkdir -p /app/media

# Entrypoint script to handle startup tasks (optional but good practice)
COPY <<EOF /entrypoint.sh
#!/bin/sh

if [ "\$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z \$POSTGRES_HOST \$POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput

exec "\$@"
EOF

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Start Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
