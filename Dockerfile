FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -e .

EXPOSE 8080

CMD ["python", "playground/main.py"]
