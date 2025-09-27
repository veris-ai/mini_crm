FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app/

# Set environment variables
ENV VERIS_API_URL=http://host.docker.internal:8742
ENV VERIS_API_VERSION=v3

# Expose port
EXPOSE 8081

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]