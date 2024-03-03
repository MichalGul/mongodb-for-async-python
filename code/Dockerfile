FROM python:3.11-slim

WORKDIR /app

COPY ./app .

RUN pip install -r requirements.txt


CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80", "--reload"]