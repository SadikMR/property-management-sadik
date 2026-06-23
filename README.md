# Property Management

A Django property listing app with geospatial search and semantic location matching.

## Quick Start

```bash
git clone https://github.com/SadikMR/property-management-sadik.git
cd property-management-sadik
cp .env.example .env
```
- clones the repository and prepares local configuration.

Edit `.env` and set `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`, and other required values.

```bash
docker compose up --build -d
```
- builds the Docker images and starts the services in the background.
- use this the first time or after changing Dockerfile / dependencies.

```bash
docker compose exec django python manage.py migrate
```
- applies Django database migrations inside the running container.

```bash
docker compose exec django python manage.py import_properties
```
- imports sample property and location data from `data/properties.csv`.

```bash
docker compose exec django python manage.py createsuperuser
```
- creates the Django admin user for managing properties and images.

Open the app at `http://localhost:8000`

### After first setup

For normal development, use:

```bash
docker compose up -d
```

- starts the existing containers in the background.
- do not use `--build` every time unless you change Dockerfile or dependencies.

## What This Project Does

- Stores locations and properties in PostgreSQL
- Uses PostGIS to store geospatial coordinates and support location-based queries
- Uses pgvector to store embeddings for semantic location matching
- Uses sentence-transformers to generate location embeddings from text
- Provides homepage autocomplete that queries semantic locations via API
- Offers a property listing page and a property detail page
- Uses pandas to import property/ location data from CSV
- Provides Django admin with inline property image upload via `PropertyImageInline`

## URL examples

- Home: `http://localhost:8000/`
- Search page: `http://localhost:8000/search/?location=Manhattan`
- Autocomplete API: `http://localhost:8000/locations/autocomplete/?q=Manhattan`

## How semantic search works here

1. `import_properties` reads `data/properties.csv` with pandas.
2. Locations are created with `name_embedding` vectors from `property_app/services/embedding.py`.
3. When the frontend sends an autocomplete query, the API calls `semantic_location_search` in `property_app/services/search.py`.
4. That function uses `pgvector` cosine distance to find locations whose stored embeddings are closest to the query embedding.
5. The API returns matching locations through `LocationAutocompleteSerializer`.


## Key Components

- `property_app/models.py`
  - `Location` stores `name`, `country`, `center`, and `name_embedding`
  - `Property` stores `title`, `slug`, `property_type`, `price`, `description`, `amenities`, and `center`
  - `PropertyImage` stores images uploaded for a property

- `property_app/services/embedding.py`
  - Loads `sentence-transformers/all-MiniLM-L6-v2`
  - Generates embeddings for location names

- `property_app/services/search.py`
  - Performs semantic location lookup using `pgvector` cosine distance
  - Returns the nearest matching locations for a typed query

- `property_app/serializers.py`
  - Defines `LocationAutocompleteSerializer`
  - Serializes autocomplete results returned by the API

- `property_app/management/commands/import_properties.py`
  - Reads `data/properties.csv` with `pandas`
  - Creates `Location` and `Property` records
  - Stores location embeddings on import

- `property_app/admin.py`
  - Registers `Property` and `PropertyImage`
  - Adds `PropertyImageInline` so images can be uploaded directly on the Property admin page

## Search and UI

- Homepage search uses semantic autocomplete, so typed location names match related locations even if the words are not exact.
- Autocomplete data comes from `LocationAutocompleteAPIView` in `property_app/views.py`.
- The homepage uses `templates/home.html` for search input and featured property grid.
- Property listing results appear in `templates/property_list.html`.
- Property detail pages show each listing with price, amenities, and location details.

## Infrastructure

- `docker-compose.yml` runs the Django app and PostgreSQL/PostGIS container.
- `docker/init.sql` creates PostGIS and pgvector extensions in the database.
- `core/settings.py` configures `MEDIA_ROOT`, `MEDIA_URL`, and database connection settings.

## Useful Commands

```bash
# start services (foreground)
docker compose up

# start services in background
docker compose up -d

# restart services
docker compose restart

# run migrations
docker compose exec django python manage.py migrate

# import data
docker compose exec django python manage.py import_properties

# create admin user
docker compose exec django python manage.py createsuperuser

# run shell
docker compose exec django python manage.py shell

# stop services
docker compose down

# rebuild and restart after Dockerfile or dependency changes
docker compose down && docker compose up --build
```

## Project Structure

```
├── core/                 # Django project settings and URL config
├── property_app/         # main app: models, views, serializers, admin, search logic
├── templates/            # UI templates for home, listing, detail pages
├── data/                 # CSV source used by import_properties command
├── docker/               # Docker build files and DB init script
├── docker-compose.yml   # service definitions
├── README.md
├── requirements.txt
```
