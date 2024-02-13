# Run a container from the built image with exposed ports
docker run -d --name meshtastic-matrix-relay-docker -p 1394:1394 -p 8000:8000 meshtastic-matrix-relay-docker:latest
