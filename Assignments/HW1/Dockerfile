# Use the official Python image with the tag 3.12-alpine as a base image
FROM python:3.12-alpine

WORKDIR /app

# Copy requirements.txt from the current directory to the container
COPY ./requirements.txt /app

# Install python3 dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory to the container
COPY . /app

# Sets app.py as the entry point for the container
ENTRYPOINT ["python3", "app.py"]
