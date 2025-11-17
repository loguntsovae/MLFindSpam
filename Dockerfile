# SMS Spam Classifier

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=ui/app.py

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Create necessary directories and clean up any conflicting files
RUN mkdir -p data models && \
    rm -rf model.pkl 2>/dev/null || true

# Train the model (or copy pre-trained model)
# Comment out if you want to train on container start instead
RUN python src/prepare.py && python src/train.py

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5001')" || exit 1

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "60", "ui.app:app"]
