FROM python:3.10

# Install unixodbc and ODBC drivers
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    # If you're connecting to a SQL Server, you might need the MS SQL Server ODBC Drivers
    # For example, to install Microsoft's ODBC Driver for SQL Server:
    # g++ (if you're compiling pyodbc or other packages from source)
    g++ \
    && apt-get clean

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME


ENV DATABASE_TYPE="mysql"
ENV TEST_TYPE="automatic"
# Before the App/ --- Set paths that match your directory
ENV ENV_PATH="C:/NextRevol/nuFa/NufaersatzteileProject/App/"




COPY . .

# Document that the service listens on port 8080.
EXPOSE 8080

CMD exec uvicorn app.main:app --workers 1 --port 8080 --host 0.0.0.0