FROM python:3.11-slim

# Keep Python logs unbuffered and avoid unnecessary bytecode files.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Run the application from a dedicated working directory.
WORKDIR /backend

# Copy dependency definitions first to leverage Docker layer caching.
COPY backend/requirements.txt ./requirements.txt

# Install backend dependencies required to run FastAPI in production.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy only the FastAPI backend source into the container.
COPY backend/ .

# Expose the FastAPI application port.
EXPOSE 8000

# Start the API server in production mode.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
