# Use the official Python 3.11 image
FROM python:3.11.2-slim

ENV PYTHONUNBUFFERED 1
# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
# COPY quart-login ./quart-login
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .
