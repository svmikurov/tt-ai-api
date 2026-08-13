FROM python:3.13-slim

WORKDIR /app

COPY requirements.system.txt .
RUN pip install --no-cache-dir -r requirements.system.txt

COPY . .

CMD ["uvicorn", "src.sd.entrypoint.main:app", "--host", "0.0.0.0", "--port", "8000"]