FROM python:3.11-slim

ARG PROJECT_NAME=inventory

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 3000

CMD ["gunicorn", "inventory.wsgi:application", "-c", "/gunicorn.conf.py", "-w", "4", "-b", "0.0.0.0:3000", "--timeout", "60"]
