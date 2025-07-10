# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose ports (Dagit, FastAPI, etc.)
EXPOSE 3000 8000

# Default command (override in docker-compose if needed)
CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]

