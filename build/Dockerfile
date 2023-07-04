# Use the official Python image as the base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 5000 for the Flask web server
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Set the label for the Docker image
LABEL org.opencontainers.image.source=https://github.com/<username>/<repository>

# Start the Flask web server
CMD ["flask", "run", "--host=0.0.0.0"]