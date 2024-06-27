# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the Docker container
WORKDIR /app

# Install the PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run the seed script when the container starts
CMD ["sh", "-c", "until pg_isready -h db -p 5432; do sleep 1; done; python seed.py"]
