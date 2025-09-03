FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "api:app", "--bind", "0.0.0.0:3000"]
