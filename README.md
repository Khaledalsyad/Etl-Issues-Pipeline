# GitHub Issues ETL Pipeline

### Production-Oriented Data Engineering Pipeline

An end-to-end ETL pipeline that extracts GitHub data through the GraphQL API, transforms and validates it, and loads it into PostgreSQL.

---

## Table of Contents

- [Architecture](#architecture)
- [Key Features](#key-features)
- [Engineering Challenges](#engineering-challenges)
- [Data Model](#data-model)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Testing](#testing)
- [Technology Stack](#technology-stack)

---

## Architecture

```text
GitHub GraphQL API
        |
        v
 GitHub Client
        |
        v
    Extract
        |
        v
   Transform
        |
        v
   Validate
        |
        v
     Load
        |
        v
  PostgreSQL
```

---

## Key Features

- GraphQL API extraction
- Cursor-based pagination
- Data transformation and validation
- Incremental processing
- Transaction management
- Idempotent loading with `ON CONFLICT`
- PostgreSQL relational data modeling
- Modular ETL architecture
- Automated testing

---

## Engineering Challenges

### API Pagination

GitHub uses cursor-based pagination. The pipeline implements reusable pagination logic using `hasNextPage` and `endCursor`.

### Transaction Safety

Multiple datasets are loaded into PostgreSQL. Transactions ensure that a failure can roll back the database changes instead of leaving a partial load.

### Idempotent Loading

Conflict-handling logic allows the pipeline to be executed repeatedly without unnecessarily creating duplicate records.

### Data Validation

Validation acts as a gate between transformation and loading to prevent invalid data from reaching PostgreSQL.

### Incremental Processing

Pipeline metadata and update timestamps are used to support processing of new and updated records instead of repeatedly processing the full dataset.

---

## Data Model

```text
Organization
     |
     v
Repository
     |
     v
Issues

Issue -------- Label
  |
  +---------- User
```

Main entities:

- Organizations
- Repositories
- Issues
- Users
- Labels
- Issue Labels
- Issue Assignees

---

## Project Structure

```text
GitHub Issues ETL Pipeline/
|
├── src/
│   ├── github_client.py
│   ├── extract.py
│   ├── transform.py
│   ├── validation.py
│   ├── load.py
│   ├── metadata.py
│   ├── scheduler.py
│   ├── graphql_queries.py
│   ├── graph_query.py
│   ├── main.py
│   └── sql/
│       └── queries.py
|
├── database/
├── diagram/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

Clone the repository:

```bash
git clone https://github.com/Khaledalsyad/Etl-Issues-Pipeline.git
cd Etl-Issues-Pipeline
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scriptsctivate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables:

```env
GITHUB_TOKEN=your_github_token
DATABASE_URL=your_postgresql_connection
GITHUB_ORGANIZATION=your_organization
GITHUB_REPOSITORY=your_repository
```

Run the pipeline:

```bash
python src/main.py
```

---

## Testing

```bash
python -m unittest discover -s tests
```

---

## Technology Stack

- Python
- PostgreSQL
- GitHub GraphQL API
- SQLAlchemy
- Pandas
- unittest

---

## Engineering Concepts

- ETL Architecture
- Data Validation
- Data Quality
- Incremental Loading
- Transactions
- Idempotency
- Relational Data Modeling
- Separation of Concerns
- Dependency Injection
- Error Handling
- Testing

---

## Author

**Khaled Abdullah Ahmed**

GitHub: https://github.com/Khaledalsyad
