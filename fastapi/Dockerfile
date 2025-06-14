# "myapi" FastAPI Services
FROM python:3.10.9-slim

WORKDIR /appdir

# wait-for-it.sh pauses FastAPI startup until postgres is listening on its port
COPY ./wait-for-it.sh /appdir/wait-for-it.sh
RUN chmod o+x /appdir/wait-for-it.sh

# Install Linux build tools to enable some Python installations
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Standard upgrades for any Python environment
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt /appdir/

# Install all Python dependencies. (NOTE: The "myapi" FastAPI application module is installed separately below)
RUN pip install --no-cache-dir -r requirements.txt

# "myapi" application module package, ready for installation
COPY ./myapi/ /appdir/myapi/

# Parquet seed data
COPY ./data/ /appdir/data/

# Entrypoint file
COPY ./main.py /appdir/

# setup.py enables pip installation of myapi app module
COPY ./setup.py /appdir/

# Install the "myapi" FastAPI application module
RUN pip install .

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

