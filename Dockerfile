FROM python:3.10-slim

# System dependencies for geospatial libraries
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Установите правильную версию GDAL для Python
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Явная установка GDAL с совместимостью
RUN pip install --no-cache-dir \
    GDAL==$(gdal-config --version | cut -d. -f1-2).0

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.serverAddress=localhost"]