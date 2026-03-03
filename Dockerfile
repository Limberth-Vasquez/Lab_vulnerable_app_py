FROM python:3.10-slim-bookworm

WORKDIR /app

COPY app.py .

RUN apt-get update && \
    apt-get install -y gcc g++ curl gnupg unixodbc-dev && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install flask pyodbc

EXPOSE 5001

CMD ["python", "app.py"]
