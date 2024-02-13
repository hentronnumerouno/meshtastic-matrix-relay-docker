#docker system prune -f
git clone https://github.com/geoffwhittington/meshtastic-matrix-relay.git
cd meshtastic-matrix-relay
git checkout v0.5.2

docker rm meshtastic-matrix-relay-docker
./build.sh
docker-compose up -d
docker logs meshtastic-matrix-relay-docker