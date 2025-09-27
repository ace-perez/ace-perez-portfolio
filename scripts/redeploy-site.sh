
#!/bin/bash

# Use the current user's home directory instead of /root
LOGDIR="$HOME/ace-perez-portfolio/errors"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/$(date +'%Y-%m-%d_%H-%M-%S').log"

echo "Going to project directory..."
cd ~/ace-perez-portfolio || exit 1

# Detect which container system is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
else
    echo "ERROR: Neither docker-compose nor podman-compose found"
    exit 1
fi

echo "Using compose command: $COMPOSE_CMD"

echo "Pulling latest code from GitHub..."
git fetch && git reset origin/main --hard

echo "Bringing down existing containers..."
docker compose -f docker-compose.prod.yml down 2>&1 | tee -a "$LOGFILE"

echo "Rebuilding and restarting containers..."
docker compose -f docker-compose.prod.yml up -d --build --force-recreate 2>&1 | tee -a "$LOGFILE"

echo "Waiting for containers to start..."
sleep 15

echo "Container status:"
docker compose -f docker-compose.prod.yml ps

echo "Checking logs..."
docker compose -f docker-compose.prod.yml logs --tail=30

echo "Site redeployed successfully!"
