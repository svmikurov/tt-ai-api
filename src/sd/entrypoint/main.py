"""FastAPI entrypoint."""

from fastapi import FastAPI

app = FastAPI(title='Demo API', version='0.1.0')


@app.get('/')
async def root():
    return {'message': 'Hello FastAPI!'}


@app.get('/health')
async def health():
    return {'status': 'ok'}