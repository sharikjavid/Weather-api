# Use official slim Python base image for minimal footprint
FROM python:3.11-slim

# Ensure stdout/stderr aren’t buffered (helps logging)
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install OS‑level dependencies (if needed for your app)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification first (leverages Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure .env variables are loaded into container
COPY .env .

# Expose application port
EXPOSE 8000

# Healthcheck endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f "http://localhost:8000/weather?latitude=40.7128&longitude=-74.0060" || exit 1


# Command to run the FastAPI app
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
