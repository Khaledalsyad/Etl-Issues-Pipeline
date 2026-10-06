# GitHub Issues ETL Pipeline

Extracts GitHub organization, repository, issue, label, user, and assignment data through GitHub GraphQL, validates it, and upserts it into PostgreSQL.

## Local setup

1. Create a virtual environment and install `pip install -r requirements.txt`.
2. Copy the required connection settings into a local `.env` file: `GITHUB_TOKEN`, `DATABASE_URL`, `GITHUB_ORGANIZATION`, and `GITHUB_REPOSITORY`.
3. Apply `database/aschema.sql`, then `database/INDEX.SQL`, to PostgreSQL.
4. Run `python src/main.py`, or schedule it with `python src/scheduler.py`.

Run checks with `python -m unittest discover -s tests`.

`DATABASE_URL` must point at PostgreSQL. Do not commit `.env`.

The schema files are for a clean database. If a database already contains the old
tables, create and review a migration before applying schema changes to production.
