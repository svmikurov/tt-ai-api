FROM python:3.13-slim

WORKDIR /docs

COPY requirements.docs.txt requirements.docs.txt
RUN pip install --no-cache-dir -r requirements.docs.txt

COPY docs/source /docs/source
RUN sphinx-build /docs/source /docs/build/html

CMD ["python", "-m", "http.server", "--directory", "/docs/build/html", "8000"]