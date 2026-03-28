# 🚀 Campaign Ingestion Backend

A scalable backend system to ingest, process, and analyze campaign data
from CSV files using FastAPI, Celery, PostgreSQL, and Redis.

------------------------------------------------------------------------

## 🧠 Architecture Overview

-   FastAPI → API layer
-   Celery → async processing
-   Redis → message broker
-   PostgreSQL → database
-   Docker Compose → orchestration

------------------------------------------------------------------------

## ⚙️ Prerequisites

-   Docker
-   Docker Compose

------------------------------------------------------------------------

## 🚀 Run the Project

``` bash
docker-compose up --build
```

------------------------------------------------------------------------

## 📤 Upload CSV

POST /upload/{platform}

Example:

``` bash
curl -X POST "http://localhost:8000/upload/meta"   -H "Content-Type: multipart/form-data"   -F "file=@sample.csv"
```

------------------------------------------------------------------------

## 📊 APIs

-   GET /jobs/{job_id}
-   GET /campaigns
-   GET /campaigns/{ad_id}


------------------------------------------------------------------------

## 🔥 Features

-   Async processing
-   Idempotent ingestion
-   Bulk upsert
-   JSONB raw fields
-   Job tracking

------------------------------------------------------------------------

## 🏁 Author

Prateek Saini
