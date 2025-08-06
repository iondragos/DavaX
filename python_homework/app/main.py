from flask import Flask, request, jsonify

from app.auth import generate_token, auth_required
from app.db import init_db, SessionLocal
from app.logger import setup_logger
from app.logger_kafka import send_log
from app.models import RequestLog
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .cache import client as redis_client

app = Flask(__name__)

request_logger = setup_logger()

#init_db()

REQUEST_COUNT = Counter(
    'math_service_requests_total',
    'Total HTTP requests processed',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'math_service_request_latency_seconds',
    'Latency of HTTP requests in seconds',
    ['endpoint']
)

def log_request_db(endpoint: str, params: dict, result):
    db = SessionLocal()
    db.add(RequestLog(
        endpoint=endpoint,
        params=str(params),
        result=str(result),
        created_at=datetime.utcnow()
    ))
    db.commit()
    db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = data.get('user')
    if not user:
        return jsonify({'error': 'Missing user field'}), 400
    token = generate_token(user)
    return jsonify({'token': token}), 200

@app.route('/pow', methods=['GET'])
@auth_required
def compute_pow():
    base = float(request.args.get('base', 0))
    exp  = float(request.args.get('exp',   1))
    key = f"pow:{base}:{exp}"
    cached = redis_client.get(key)
    if cached:
        res = float(cached)
    else:
        with REQUEST_LATENCY.labels(endpoint='pow').time():
            res = float(base) ** float(exp)
        redis_client.setex(key, 60, res)

    REQUEST_COUNT.labels(method='GET', endpoint='pow', http_status=200).inc()

    log_request_db('pow', {'base': base, 'exp': exp}, res)
    log_payload = {'endpoint': 'pow', 'params': {'base': base, 'exp': exp}, 'result': res}
    request_logger.info(log_payload)
    send_log(log_payload)

    return jsonify({'result': res})

@app.route('/fib/<int:n>', methods=['GET'])
@auth_required
def compute_fib(n):
    key = f"fib:{n}"
    cached = redis_client.get(key)
    if cached:
        a = int(cached)
    else:
        with REQUEST_LATENCY.labels(endpoint='fib').time():
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
        redis_client.setex(key, 60, a)

    REQUEST_COUNT.labels(method='GET', endpoint='fib', http_status=200).inc()

    log_request_db('fib', {'n': n}, a)
    log_payload = {'endpoint': 'fib', 'params': {'n': n}, 'result': a}
    request_logger.info(log_payload)
    send_log(log_payload)

    return jsonify({'result': a})

@app.route('/fact/<int:n>', methods=['GET'])
@auth_required
def compute_fact(n):
    key = f"fact:{n}"
    cached = redis_client.get(key)
    if cached:
        result = int(cached)
    else:
        with REQUEST_LATENCY.labels(endpoint='fact').time():
            result = 1
            for i in range(2, n + 1):
                result *= i
        redis_client.setex(key, 60, result)

    REQUEST_COUNT.labels(method='GET', endpoint='fact', http_status=200).inc()

    log_request_db('fact', {'n': n}, result)
    log_payload = {'endpoint': 'fact', 'params': {'n': n}, 'result': result}
    request_logger.info(log_payload)
    send_log(log_payload)

    return jsonify({'result': result})

@app.route('/metrics')
def metrics():
    data = generate_latest()
    return data, 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)