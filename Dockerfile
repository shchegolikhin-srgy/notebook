FROM python:3.13-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY app/ .

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
