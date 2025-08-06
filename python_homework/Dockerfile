FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p logs

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

RUN python3 -c "from app.db import init_db; init_db()"

EXPOSE 5000

CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000", "--workers", "4"]