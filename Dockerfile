# Official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src

# Ensure the app package is on PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Start the app with uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
