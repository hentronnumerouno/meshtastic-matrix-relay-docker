# meshtastic-matrix-relay-docker
### A simple fork of the awesome https://github.com/geoffwhittington/meshtastic-matrix-relay.git project but in a more portable version using Docker!

### Deployment Guide
Step 1: Clone this git repo
`git clone https://github.com/hentronnumerouno/meshtastic-matrix-relay-docker.git`

Step 2: Update your config.yaml file within the "meshtastic-matrix-relay" folder

Step 3: Deploy the container!
`chmod +x deploy.sh && ./deploy.sh`

Notes: This code naturally does not update to the latest branch of https://github.com/geoffwhittington/meshtastic-matrix-relay so it remains stable. However, when ready to upgrade to the latest version of the true software doing all of the heavy lifting simply execute `update.sh`. This will append the "outdated" name on the incumbent version before downloading the latest and greatest release from https://github.com/geoffwhittington/meshtastic-matrix-relay. The latest known working commit is 2b39884 however future releases will likely work.
