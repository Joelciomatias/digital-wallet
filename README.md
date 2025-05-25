# 🚀 digital-wallet API

Basic API using [FastAPI](https://fastapi.tiangolo.com/) with Docker Compose.

---

## 📚 API Documentation

The application will be available at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## 📦 Requirements

- Python 3.10+
- Docker and Docker Compose installed

---

## ⚙️ Setup

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Run the application:

```bash
python -m uvicorn app.main:app --reload
```

### 🔧 Docker

Build the Docker image:

```bash
docker-compose build
```

Run the container:

```bash
docker-compose up
```