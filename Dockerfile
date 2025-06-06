FROM python:3.13-alpine

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]