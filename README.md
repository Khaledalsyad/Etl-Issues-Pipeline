# GitHub Issues ETL Pipeline

A production-oriented Data Engineering pipeline that extracts GitHub
organization, repository, issue, label, user, and assignment data
through the GitHub GraphQL API, transforms and validates the data, and
loads it into PostgreSQL.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Key Engineering Features](#key-engineering-features)
- [Data Flow](#data-flow)
- [Data Model](#data-model)
- [Project Structure](#project-structure)
- [Transaction Management](#transaction-management)
- [Incremental Processing](#incremental-processing)
- [Idempotent Loading](#idempotent-loading)
- [Validation](#validation)
- [Testing](#testing)
- [Installation](#installation)
- [Running the Pipeline](#running-the-pipeline)
- [Technology Stack](#technology-stack)
- [Engineering Concepts](#engineering-concepts)

## Project Overview

This project demonstrates an end-to-end ETL workflow:
<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![GraphQL](https://img.shields.io/badge/API-GraphQL-e10098?logo=graphql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)
![Tests](https://img.shields.io/badge/Tests-unittest-green)

</p>

1.  Extract data from GitHub using GraphQL.
2.  Handle cursor-based pagination.
3.  Transform nested API responses into structured datasets.
4.  Validate transformed data before loading.
5.  Load validated data into PostgreSQL.
6.  Use transactions to prevent partial loads.
7.  Support incremental processing.
8.  Use conflict-handling logic for idempotent loading.
9.  Maintain pipeline metadata.

## Architecture

``` text
                    GitHub GraphQL API
                           |
                           v
                  +-------------------+
                  |   GitHub Client   |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |     Extractor     |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |    Transformer    |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |    Validation     |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |      Loader       |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |    PostgreSQL     |
                  +-------------------+
                           |
                           v
                  +-------------------+
                  |     Metadata      |
                  +-------------------+
```

## End-to-End Data Flow

``` text
GitHub GraphQL
      |
      | Extract
      v
Raw API Response
      |
      | Transform
      v
Structured DataFrames
      |
      | Validate
      v
Validated DataFrames
      |
      | Load
      v
PostgreSQL
```

## Main Responsibilities

### Extract

The Extract layer communicates with the GitHub GraphQL API.

Responsibilities:

-   Execute GraphQL queries.
-   Extract organization data.
-   Extract repository data.
-   Extract issues.
-   Handle cursor-based pagination.
-   Preserve source data structure.
-   Propagate required source identifiers.

### Transform

The Transform layer prepares raw API data for the target database.

Responsibilities:

-   Clean source data.
-   Flatten nested GraphQL responses.
-   Extract nested entities.
-   Build structured DataFrames.
-   Build relationship datasets.
-   Add required audit information.
-   Prepare data according to the target data model.

### Validation

Validation is the quality gate between transformation and loading.

``` text
              Transform
                  |
                  v
             Validation
              /               Invalid      Valid
            |           |
            v           v
          STOP         Load
```

Validation checks include:

-   Expected columns.
-   Required columns.
-   Required NULL constraints.
-   Duplicate records.
-   Primary key integrity.
-   Data contract consistency.

Invalid data should not reach PostgreSQL.

### Load

The Load layer writes validated data into PostgreSQL.

``` text
DataFrame
    |
    v
Validation
    |
    v
Convert to Records
    |
    v
Select SQL Query
    |
    v
Execute
    |
    v
PostgreSQL
```

SQL statements are separated from loading logic to improve
maintainability and testing.

## Transaction Management

Database loading is performed using transactions.

``` text
BEGIN
  |
  +-- Load Organization
  +-- Load Repository
  +-- Load Users
  +-- Load Issues
  +-- Load Labels
  +-- Load Relationships
  |
  v
SUCCESS?
 /     YES     NO
 |       |
COMMIT  ROLLBACK
```

If an error occurs during the transaction, the transaction is rolled
back instead of leaving the database partially loaded.

## Idempotent Loading

The pipeline is designed to support safe reruns.

Database operations use conflict-handling mechanisms such as:

``` sql
ON CONFLICT
```

This allows existing records to be handled without unnecessarily
creating duplicates.

``` text
First Run
    |
    v
Insert Records
    |
    v
Database

Second Run
    |
    v
Same / Updated Records
    |
    v
ON CONFLICT
    |
    v
Update / Ignore
```

## Incremental Processing

The pipeline supports incremental processing using update timestamps.

``` text
Previous Processing State
          |
          v
      GitHub API
          |
          v
New / Updated Records
          |
          v
       Transform
          |
          v
       Validate
          |
          v
         Load
```

This reduces unnecessary extraction and makes the pipeline suitable for
recurring execution.

## Pagination

The pipeline uses cursor-based pagination.

``` text
Request
   |
   v
Page 1
   |
   +---- hasNextPage = True
   |             |
   |             v
   |          endCursor
   |             |
   |             v
   |          Page 2
   |
   +---- hasNextPage = False
                 |
                 v
                Stop
```

Pagination logic is separated from entity-specific extraction logic so
it can be reused.

## Data Model

The pipeline works with GitHub entities and their relationships.

Core entities:

``` text
Organization
     |
     v
Repository
     |
     v
Issues
```

Additional entities:

``` text
Users
Labels
```

Many-to-many relationships:

``` text
Issue
  |
  +------ Issue Label ------ Label
  |
  +------ Issue Assignee --- User
```

This structure preserves relational integrity.

## Project Structure

``` text
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
│   |
│   └── sql/
│       └── queries.py
|
├── database/
│   ├── aschema.sql
│   └── INDEX.SQL
|
├── diagram/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Component Responsibilities

  Component              Responsibility
  ---------------------- ---------------------------------------------
  `github_client.py`     Communicates with GitHub GraphQL API
  `extract.py`           Extracts source data and handles pagination
  `transform.py`         Cleans and restructures source data
  `validation.py`        Validates transformed datasets
  `load.py`              Loads validated data into PostgreSQL
  `metadata.py`          Manages pipeline processing metadata
  `graphql_queries.py`   Stores GraphQL queries
  `graph_query.py`       GraphQL query-related definitions
  `sql/queries.py`       Stores SQL statements
  `main.py`              Orchestrates the ETL pipeline
  `scheduler.py`         Supports scheduled pipeline execution

## Separation of Concerns

``` text
GitHub Client
     |
     | API Communication
     v
Extractor
     |
     | Source Extraction
     v
Transformer
     |
     | Data Preparation
     v
Validation
     |
     | Data Quality Gate
     v
Loader
     |
     | Database Operations
     v
PostgreSQL
```

Each layer has a clearly defined responsibility.

## Dependency Injection

Dependencies are created at the application entry point and passed into
the required components.

``` text
                main.py
                   |
          +--------+--------+
          |                 |
          v                 v
   GitHub Client       Database Engine
          |                 |
          v                 v
      Extractor           Loader
```

This reduces coupling and makes components easier to test and replace.

## Data Contract

The pipeline maintains a data contract between its layers.

``` text
Transform
    |
    | Data Contract
    v
Validation
    |
    | Data Contract
    v
SQL / Loader
    |
    | Data Contract
    v
PostgreSQL Schema
```

Expected columns, keys, relationships, and data types must remain
consistent.

## Error Handling

Critical failures stop downstream processing.

Examples:

-   GitHub API extraction failures.
-   Invalid GraphQL responses.
-   Missing required data.
-   Validation failures.
-   Database execution errors.
-   Transaction failures.

``` text
Extract Failed
      |
      v
   STOP

Transform Failed
      |
      v
   STOP

Validation Failed
      |
      v
   STOP

Load Failed
      |
      v
 ROLLBACK
```

## Configuration

Sensitive configuration should be stored in environment variables.

``` env
GITHUB_TOKEN=your_github_token
DATABASE_URL=your_postgresql_connection
GITHUB_ORGANIZATION=your_organization
GITHUB_REPOSITORY=your_repository
```

Do not commit `.env` to the repository.

## Local Setup

### 1. Clone the Repository

``` bash
git clone https://github.com/Khaledalsyad/Etl-Issues-Pipeline.git
cd Etl-Issues-Pipeline
```

### 2. Create a Virtual Environment

``` bash
python -m venv .venv
```

Windows:

``` bash
.venv\Scripts\activate
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file:

``` env
GITHUB_TOKEN=your_github_token
DATABASE_URL=your_postgresql_connection
GITHUB_ORGANIZATION=your_organization
GITHUB_REPOSITORY=your_repository
```

### 5. Prepare PostgreSQL

Apply the database schema files:

``` text
database/aschema.sql
database/INDEX.SQL
```

## Running the Pipeline

``` bash
python src/main.py
```

For scheduled execution:

``` bash
python src/scheduler.py
```

## Testing

``` bash
python -m unittest discover -s tests
```

## Technology Stack

-   Python
-   PostgreSQL
-   GitHub GraphQL API
-   SQLAlchemy
-   Pandas
-   GraphQL
-   unittest
-   Git

## Engineering Concepts Demonstrated

### Data Engineering

-   ETL Architecture
-   API Data Extraction
-   GraphQL
-   Cursor-based Pagination
-   Incremental Loading
-   Data Transformation
-   Data Validation
-   Data Quality
-   Data Modeling
-   PostgreSQL
-   Metadata Management

### Database Engineering

-   Relational Data Modeling
-   Primary Keys
-   Foreign Keys
-   Many-to-Many Relationships
-   Upsert Operations
-   `ON CONFLICT`
-   Transactions
-   Commit / Rollback
-   Referential Integrity

### Software Engineering

-   Separation of Concerns
-   Single Responsibility Principle
-   Dependency Injection
-   Modular Architecture
-   Reusable Components
-   Error Handling
-   Logging
-   Automated Testing

## Design Principles

### Single Responsibility

Each component has a focused responsibility.

### Separation of Concerns

API communication, extraction, transformation, validation, and database
operations are separated.

### Fail Fast

Critical failures stop the pipeline instead of allowing invalid data to
continue downstream.

### Transaction Safety

Related database operations are grouped into transactions to prevent
partial loads.

### Idempotency

The pipeline is designed to safely handle repeated executions.

### Reusability

Common logic such as pagination and database operations is implemented
in reusable components.

## Pipeline Execution Model

``` text
                  START
                    |
                    v
             GitHub GraphQL
                    |
                    v
                EXTRACT
                    |
                    v
               TRANSFORM
                    |
                    v
               VALIDATE
                    |
              +-----+-----+
              |           |
           INVALID       VALID
              |           |
              v           v
             STOP        LOAD
                           |
                           v
                      TRANSACTION
                           |
                    +------+------+
                    |             |
                 SUCCESS        ERROR
                    |             |
                    v             v
                  COMMIT       ROLLBACK
                    |
                    v
                  DONE
```

## Project Goal

The goal is not simply to retrieve GitHub data.

The goal is to demonstrate how to design and implement a structured Data
Engineering pipeline that moves data from an external API into a
relational database while maintaining:

-   Data quality
-   Data integrity
-   Transaction safety
-   Idempotency
-   Incremental processing
-   Maintainability
-   Clear separation of responsibilities

``` text
External API
     ↓
Extraction
     ↓
Transformation
     ↓
Validation
     ↓
Database Loading
     ↓
PostgreSQL
```

## Author

**Khaled Abdullah Ahmed**

GitHub: https://github.com/Khaledalsyad
