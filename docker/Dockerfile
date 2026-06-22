# PostgreSQL image
FROM postgres:17 AS postgres

RUN apt-get update && \
    apt-get install -y \
    postgresql-17-postgis-3 \
    postgresql-17-postgis-3-scripts \
    postgresql-17-pgvector && \
    rm -rf /var/lib/apt/lists/*


# Django image
FROM python:3.12-slim AS django

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]