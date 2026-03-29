# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the project in editable mode (for tool discovery)
RUN pip install -e .

# Expose the ports (Only 8501 is public, 8000 is internal)
EXPOSE 8501
EXPOSE 8000

# Make start script executable
RUN chmod +x start.sh

# Start both services via an orchestrator script
CMD ["./start.sh"]
