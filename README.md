# Property Management

A Django app for managing property listings with location-based search. Uses PostGIS for geospatial queries and pgvector for semantic search.

## Tech Stack

- Django + Django REST Framework
- PostgreSQL with PostGIS and pgvector extensions
- Docker

## Getting Started

Clone the repo and cd into it:

```bash
git clone https://github.com/SadikMR/property-management-sadik.git
cd property-management-sadik
```

Copy the example env file and update values:

```bash
cp .env.example .env
```

Open `.env` and set your own `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`. The defaults work fine for local dev.

Build and start everything:

```bash
docker compose up --build
```

First time setup — run migrations and import sample data:

```bash
docker compose exec django python manage.py migrate
docker compose exec django python manage.py import_properties
```

App runs at http://localhost:8000

## Project Structure

```
├── core/                  # django project settings
├── property_app/          # main app (models, views, urls)
├── templates/             # html templates
├── data/                  # csv data for import
├── docker/
│   ├── Dockerfile         # postgres + django images
│   └── init.sql           # auto-creates postgis & vector extensions
├── docker-compose.yml
├── .env                   # secrets (not committed)
├── .env.example           # template for .env
└── requirements.txt
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev key |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `*` |
| `POSTGRES_USER` | DB username | `postgres` |
| `POSTGRES_PASSWORD` | DB password | — |
| `POSTGRES_DB` | DB name | `appdb` |
| `POSTGRES_HOST` | DB host | `postgres` |
| `POSTGRES_PORT` | DB port | `5432` |

## About the App

The app stores properties with their geographic coordinates. Each property belongs to a location (like "Manhattan" or "Dubai"), and each location belongs to a country.

Properties are imported from `data/properties.csv` using `python manage.py import_properties`. Each row creates a Location (with a center point) and a Property (with its own coordinates). PostGIS handles storing geo points and calculating distances. pgvector is set up for semantic search on location names using embeddings.

**Pages:**

- `/` — home page, shows all properties in a paginated grid. Search by location name, grid updates via AJAX without full page reload.
- `/search/?location=...` — filters properties by location name with pagination.
- `/property/<slug>/` — property detail page with price, type, description, amenities, and distance from location center.

## Useful Commands

```bash
# stop everything
docker compose down

# restart
docker compose down && docker compose up --build

# run in background
docker compose up --build -d

# check running containers
docker compose ps

# view logs
docker compose logs -f

# view logs for a specific service
docker compose logs -f django
docker compose logs -f postgres

# open django shell
docker compose exec django python manage.py shell

# create superuser
docker compose exec django python manage.py createsuperuser

# run migrations
docker compose exec django python manage.py migrate

# connect to database
docker compose exec postgres psql -U postgres -d appdb

# check installed extensions
docker compose exec postgres psql -U postgres -d appdb -c "\dx"

# fresh start (deletes all data)
docker compose down -v
docker compose up --build
```
