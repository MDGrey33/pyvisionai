FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed, e.g., for image processing)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --only main --no-root --no-interaction --no-ansi

# Copy the application code
COPY . /app

# Expose the port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "pyvisionai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
