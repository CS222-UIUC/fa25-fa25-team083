FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tools and curl (curl is used by docker-compose healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest first to leverage Docker cache
COPY pyproject.toml ./

# Upgrade pip and install project dependencies declared in pyproject.toml
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .

# Copy application source
COPY . .

EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
