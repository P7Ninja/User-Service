FROM python:3.10-alpine

WORKDIR /application

COPY requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

COPY /src/userservice /application/userservice
COPY /app/server.py /application/server.py

EXPOSE 8443


CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7006", "--root-path", "/userservice"]