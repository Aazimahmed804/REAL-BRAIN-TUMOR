FROM python:3.12-slim

WORKDIR /app

# System dependencies (needed for some ML libraries)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Make sure uploads folder exists
RUN mkdir -p uploads

EXPOSE 5000

CMD ["python", "app.py"]
