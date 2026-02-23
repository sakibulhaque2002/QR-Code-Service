FROM python:3.12-slim

# Install system dependencies for CairoSVG
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

#docker run -p 8000:8000 saaaakibbb/qr-code-service:latest