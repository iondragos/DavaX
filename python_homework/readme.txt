Math Operations Microservice – README
======================================

This microservice exposes three mathematical operations—power, Fibonacci,
and factorial—via a REST API while showcasing production‑grade
engineering practices in a compact stack.

ARCHITECTURE
------------
• **Flask** serves the HTTP API, organized with clear separation of concerns.  
• **Gunicorn** runs multiple WSGI workers for production robustness.  
• **SQLite** stores every request (endpoint, parameters, result, timestamp).  
• **Redis** caches computed results (60s TTL) to speed up repeats.  
• **Prometheus** scrapes `/metrics` to collect request counters & latency histograms.  
• **Kafka(+Zookeeper)** streams JSON logs to topic`math‑requests` for real‑time processing.  
• **Docker&DockerCompose** build and orchestrate the entire stack; Rancher Desktop or
  any Docker engine can run it identically.  
• **JWT** secures endpoints; clients obtain tokens at `/login` and pass
  `Authorization:Bearer<token>`.  
• **Rotating JSON file logs** provide local diagnostics; payload mirrors the
  Kafka message.

KEY FILES / FOLDERS
-------------------
| Path                    | Purpose                                           |
|-------------------------|---------------------------------------------------|
| `app/main.py`           | Routes, caching, metrics, auth, DB+Kafka logging|
| `app/models.py` & `db.py`| SQLAlchemy ORM & session setup                   |
| `app/cache.py`          | Redis client                                      |
| `app/auth.py`           | JWT helpers & decorator                           |
| `app/logger.py`         | Rotating JSON file logger                         |
| `app/logger_kafka.py`   | Kafka producer                                    |
| `Dockerfile`            | Builds service image, initializes DB schema       |
| `docker-compose.yml`    | One‑command stack: math_service, Redis, Kafka, Zoo|
| `prometheus.yml`        | Minimal Prometheus scrape config                  |

RUNNING LOCALLY
---------------
```bash
# Start the whole stack
docker-compose build
docker-compose up -d

# Get a JWT
curl -X POST http://localhost:5000/login \
     -H "Content-Type: application/json" \
     -d '{"user":"alice"}'

# Call an endpoint (replace <token>)
curl "http://localhost:5000/pow?base=2&exp=5" \
     -H "Authorization: Bearer <token>"
