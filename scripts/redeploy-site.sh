
#!/bin/bash

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
$COMPOSE_CMD -f docker-compose.prod.yml down 2>> "$LOGFILE"

echo "Rebuilding and restarting containers..."
$COMPOSE_CMD -f docker-compose.prod.yml up -d --build 2>> "$LOGFILE"

echo "Container status:"
$COMPOSE_CMD -f docker-compose.prod.yml ps

echo "Site redeployed successfully!"
