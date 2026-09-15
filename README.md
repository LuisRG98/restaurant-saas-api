# Restaurant Management API

A production-oriented REST API for restaurant management, built with Python and FastAPI.

## 🎯 Project Goal

The goal of this project is to build a scalable backend system for managing restaurant operations while applying production-oriented software engineering practices.

## 🚀 Current Features

* Health check endpoint
* Restaurant management API
* Request validation with Pydantic
* PostgreSQL integration
* SQLAlchemy ORM
* Layered architecture
* Automated tests

## 🛠️ Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Pytest
* Docker

## 🏗️ Architecture

```text
Client
  ↓
FastAPI
  ↓
API Router
  ↓
Service Layer
  ↓
Repository Layer
  ↓
PostgreSQL
```

## ▶️ Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd restaurant-saas-api
```

### 2. Create the virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once the application is running:

* Swagger: `/docs`
* ReDoc: `/redoc`

## 🧪 Running Tests

```bash
pytest
```

## 📌 Roadmap

* [x] Project initialization
* [x] FastAPI foundation
* [ ] Restaurant persistence
* [ ] Authentication
* [ ] Role-based authorization
* [ ] Product management
* [ ] Order management
* [ ] Inventory management
* [ ] Automated CI/CD
* [ ] AWS deployment
