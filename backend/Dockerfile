FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["daphne", "config.asgi:application", "--bind", "0.0.0.0", "--port", "8000"]