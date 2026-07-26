# Sports League API Project

This project is an evolving one for my backend roadmap using Python & Django. It's a sports league manager that deals with leagues, teams, players, matches with their result and standings.

---

## Project Structure

```text
sports-league-api/
│
├── config/                  # Django project configuration
│   ├── settings.py          # Main settings (database settings, DRF, logging)
│   ├── urls.py              # Root URL routing (includes leagues & Swagger UI)
│   └── ...
│
├── leagues/                 # Core application for managing the sports league
│   ├── management/          # Custom Django admin commands
│   │   └── commands/
│   │       ├── seed_data.py         # Database seeder script
│   │       ├── compute_standings.py # Compute standings command
│   │       ├── league_report.py     # Generate league reports
│   │       └── query_practice.py    # SQL query practice command
│   ├── tests/               # pytest suite containing unit and integration tests
│   ├── filters.py           # Custom API query filters (DjangoFilterBackend)
│   ├── models.py            # Database models (League, Team, Player, Match, MatchResult)
│   ├── serializers.py       # DRF serializers (handles validation & representation)
│   ├── services.py          # Core business logic (dynamic standings calculations)
│   ├── urls.py              # App-specific API routing
│   └── views.py             # ViewSets implementing ModelViewSet for CRUD
│
├── utils/                   # General helper functions and utilities
│   ├── exception_handlers.py# Custom global API exception formatter
│   ├── decorators.py        # Utility decorators
│   └── validators.py        # Common data validators
│
├── Makefile                 # Command shortcuts (setup, run, test, format, lint)
├── requirements.txt         # Project Python dependencies
├── pytest.ini               # pytest test runner configuration
└── .flake8                  # flake8 linting style rules
```

---

## Tech Stack
- Python
- Django
- DRF
- PostgreSQL

---

## Prerequisites
- Python 3.12+
- PostgreSQL
- WSL2

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/andrew-remon/sports-league-api
cd sports-league-api
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/WSL2
# Or: .venv\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Or using the Makefile:
make install
```

### 4. Create Database
Create a PostgreSQL database named `sports_league`:
```bash
createdb sports_league
# Or via psql:
# CREATE DATABASE sports_league;
```

> [!IMPORTANT]
> The database connection settings are located in settings.py. By default, it expects a PostgreSQL user named `andrew` with password `12349876`. You must configure your local PostgreSQL credentials or update the `DATABASES` setting in `settings.py` to match your environment.

### 5. Migrate
Apply database migrations:
```bash
python manage.py migrate
# Or using the Makefile:
make migrate
```

### 6. Seed the Data
Seed the database with initial leagues, teams, and players:
```bash
python manage.py seed_data
# Or using the Makefile:
make seed
```

---

## Run the server
In the terminal, run the following command to start the server:
```bash
python manage.py runserver
# Or using the Makefile:
make run
```

---

## Running Tests
Run the pytest suite to verify all endpoints and logic work correctly:
```bash
pytest -v
# Or using the Makefile:
make test
```

---

## Development Workflow (Makefile)
The project includes a `Makefile` with helper commands for common actions:
- `make install` - Install dependencies from `requirements.txt`
- `make migrate` - Run database migrations
- `make seed` - Seed the database with sample data
- `make run` - Start the local Django development server
- `make test` - Run the test suite with pytest
- `make lint` - Lint files with flake8
- `make format` - Format files with black
- `make check` - Run format, lint, and tests sequentially
- `make shell` - Open Django Shell in terminal

---

## API Documentation Link

To view your schema, API endpoints, explanation of every endpoint:
1. run the server
2. In your browser, surf this link: http://localhost:8000/api/v1/schema/swagger-ui/

---

## API Endpoints Summary

| Method | Endpoint | Description | Query Parameters & Features |
|---|---|---|---|
| **Health & Metadata** | | | |
| `GET` | `/api/health/` | Health check endpoint | Returns API status and version |
| `GET` | `/api/schema/` | OpenAPI schema file | Returns raw OpenAPI JSON/YAML |
| `GET` | `/api/schema/swagger-ui/` | Swagger interactive documentation | Interactive API client |
| `GET` | `/api/schema/redoc/` | ReDoc API documentation | Structured API documentation |
| **Leagues** | | | |
| `GET` | `/api/v1/leagues/` | List all leagues | Search (`name`), Order (`name`, `created_at`) |
| `POST` | `/api/v1/leagues/` | Create a new league | - |
| `GET` | `/api/v1/leagues/{id}/` | Retrieve a league | - |
| `PUT` | `/api/v1/leagues/{id}/` | Update a league | - |
| `PATCH` | `/api/v1/leagues/{id}/` | Partially update a league | - |
| `DELETE` | `/api/v1/leagues/{id}/` | Delete a league | - |
| `GET` | `/api/v1/leagues/{id}/standings/` | Retrieve league standings | Dynamically computes standings table |
| **Teams** | | | |
| `GET` | `/api/v1/teams/` | List all teams | Filter (`league`, `city`), Search (`name`, `city`), Order (`name`, `founded_year`) |
| `POST` | `/api/v1/teams/` | Create a new team | - |
| `GET` | `/api/v1/teams/{id}/` | Retrieve a team | Prefetches players & league details |
| `PUT` | `/api/v1/teams/{id}/` | Update a team | - |
| `PATCH` | `/api/v1/teams/{id}/` | Partially update a team | - |
| `DELETE` | `/api/v1/teams/{id}/` | Delete a team | - |
| `GET` | `/api/v1/teams/{id}/players/` | List all players in a team | - |
| **Players** | | | |
| `GET` | `/api/v1/players/` | List all players | Filter (`team`, `position`, `league`), Search (`first_name`, `last_name`), Order (`last_name`, `jersey_number`) |
| `POST` | `/api/v1/players/` | Create a new player | - |
| `GET` | `/api/v1/players/{id}/` | Retrieve a player | - |
| `PUT` | `/api/v1/players/{id}/` | Update a player | - |
| `PATCH` | `/api/v1/players/{id}/` | Partially update a player | - |
| `DELETE` | `/api/v1/players/{id}/` | Delete a player | - |
| **Matches** | | | |
| `GET` | `/api/v1/matches/` | List all matches | Filter (`league`, `status`, `match_day`, `scheduled_date` range), Search (`home_team__name`, `away_team__name`), Order (`scheduled_date`, `match_day`) |
| `POST` | `/api/v1/matches/` | Create a new match | - |
| `GET` | `/api/v1/matches/{id}/` | Retrieve a match | Includes match results nested if completed |
| `PUT` | `/api/v1/matches/{id}/` | Update a match | - |
| `PATCH` | `/api/v1/matches/{id}/` | Partially update a match | - |
| `DELETE` | `/api/v1/matches/{id}/` | Delete a match | - |
| `POST` | `/api/v1/matches/{id}/record_result/` | Record match score result | Request body: scores. Marks status as `COMPLETED`. |
