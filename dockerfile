# Use a different Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for PostgreSQL support)
RUN apk add --no-cache gcc musl-dev postgresql-dev

# Copy the requirements file into the container

COPY ./celery_app/ .
COPY requirements.txt .
# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

