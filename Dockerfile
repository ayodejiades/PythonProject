FROM python:3.11-slim

# Install system dependencies
# ffmpeg is CRITICAL for audio conversion (OGG -> WAV)
# libpq-dev and gcc are needed for psycopg2 and other python extensions
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements followed by the rest of the application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
