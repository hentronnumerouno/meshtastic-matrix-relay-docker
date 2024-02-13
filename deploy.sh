#docker system prune -f
docker rm meshtastic-matrix-relay-docker
./build.sh
docker-compose up -d
docker logs meshtastic-matrix-relay-docker