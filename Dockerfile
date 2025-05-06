FROM python:3.13-slim

WORKDIR /app

COPY app/requirements.txt .

# docker build -t app-v1 .
# docker run -d -p 8080:8080 app-v1

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]