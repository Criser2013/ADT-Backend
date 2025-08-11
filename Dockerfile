FROM python:3.13.5-bullseye

WORKDIR /app/backend

COPY . .

RUN apt update && apt upgrade -y

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --no-input -r requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "./app/main.py", "--host", "0.0.0.0", "--port", "80"]