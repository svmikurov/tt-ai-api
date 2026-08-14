"""FastAPI entrypoint."""

from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title='Demo API', version='0.1.0')
engine = create_engine(DATABASE_URL)


@app.get('/')
async def root():
    return {'message': 'Hello FastAPI!'}


@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.get('/db-check')
async def db_check():
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        return {"status": "connected", "result": result.scalar()}