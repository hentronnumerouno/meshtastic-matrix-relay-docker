# Use an official Python 3.10 image as base image
FROM python:3.10

# Set the working directory within the container to the app directory
WORKDIR /app

# Copy the local git repository to the app directory inside the container
COPY meshtastic-matrix-relay/ .

# Install required packages mentioned in requirements.txt
RUN pip install -r requirements.txt

# Expose ports for Meshtastic and Matrix
EXPOSE 1394 8000

# Set the entrypoint script to start the application using python3
ENV CONFIG_FILE=config.yaml
ENTRYPOINT ["python", "main.py"]
