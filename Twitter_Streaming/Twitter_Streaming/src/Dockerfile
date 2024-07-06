# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /src

# Copy only the requirements.txt file initially to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Set environment variable to specify the location of the Flask application
ENV FLASK_APP=/src/app/app.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define default command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
