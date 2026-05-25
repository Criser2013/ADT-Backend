FROM python:3.13.5-slim-bullseye
WORKDIR /app

RUN apt update && apt install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1000 backend-user
COPY --chown=backend-user:backend-user . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --no-input -r requirements.txt
USER backend-user
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s CMD curl -H "Origin: localhost" -o /dev/null -s -w "%{http_code}\n" localhost:5000/healthcheck || exit 1
CMD ["fastapi", "run", "./app/main.py", "--host", "0.0.0.0", "--port", "80"]