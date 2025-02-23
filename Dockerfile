# Base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY converter.py .
COPY web ./web
COPY cli ./cli

# Install CLI globally
RUN chmod +x /app/cli/cli.py && \
    ln -s /app/cli/cli.py /usr/local/bin/mp4-to-gif

# Create uploads directory
RUN mkdir -p /app/uploads && \
    chmod 777 /app/uploads

# Environment variables
ENV FLASK_APP=web.app
ENV FLASK_ENV=production
ENV UPLOAD_FOLDER=/app/uploads

# Expose web interface port
EXPOSE 5000

# Volume for uploads
VOLUME ["/app/uploads"]

# Default command (run web interface)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "web.app:app"]