ARG FRONT_URL

ARG FIREBASE_CREDS

FROM python:3.13.2-alpine3.21

WORKDIR /app/backend

COPY . .

ENV FRONT_URL=${FRONT_URL}

ENV FIREBASE_CREDS=${FIREBASE_CREDS}

RUN echo "${FIREBASE_CREDS}" > firebase_tokens.json

RUN chmod +x install.sh && ./install.sh

RUN rm install.sh

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --no-input -r requirements.txt

EXPOSE 80

CMD ["fastapi", "run", "./app/main.py", "--host", "0.0.0.0", "--port", "80"]