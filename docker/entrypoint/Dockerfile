FROM python:3.12-slim

# Устанавливаем зависимости для сборки psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.system.txt .
RUN pip install --no-cache-dir -r requirements.system.txt

COPY . .

CMD ["uvicorn", "src.sd.entrypoint.main:app", "--host", "0.0.0.0", "--port", "8000"]