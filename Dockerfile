FROM python:3.13.5-bullseye
RUN apt update && apt install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m backend-user
WORKDIR /home/backend-user/backend
COPY . .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --no-input -r requirements.txt
RUN chown -R backend-user:backend-user /home/backend-user
USER backend-user
EXPOSE 80
CMD ["fastapi", "run", "./app/main.py", "--host", "0.0.0.0", "--port", "80"]