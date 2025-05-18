# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY ./src /app/src
COPY ./migrations /app/migrations
# We will mount the instance folder as a volume in docker-compose to persist the SQLite DB
# COPY ./instance /app/instance 
COPY ./entrypoint.sh /app/entrypoint.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (can be overridden by docker-compose or .env file)
ENV FLASK_APP="src.main:create_app"
ENV FLASK_ENV="development"

# Ensure the instance folder exists and entrypoint is executable
RUN mkdir -p /app/instance && chmod +x /app/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

