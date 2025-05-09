# Use the official Python 3.10 image
FROM python:3.10.12-slim

# Install system dependencies including skopeo and any other required tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    skopeo \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (excluding what's in .dockerignore)
COPY . .

# The actual application is in src/, so we might need to adjust PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port Uvicorn will run on
EXPOSE 8000

# Command to run the application
# Using the module syntax for better path handling
CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8000"]
