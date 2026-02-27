FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN apt-get update && \
    apt-get install -y gcc g++ curl gnupg unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install flask pyodbc

EXPOSE 5001

CMD ["python", "app.py"]
