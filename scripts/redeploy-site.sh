#!/bin/bash

LOGDIR="/root/flask-portfolio/errors"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/$(date +'%Y-%m-%d_%H-%M-%S').log"

echo "Going to project directory..."
cd ~/flask-portfolio || exit 1

# echo "Pulling latest code from GitHub..."
# git fetch && git reset origin/main --hard

echo "Bringing down existing containers..."
docker compose -f docker-compose.prod.yml down 2>> "$LOGFILE"

echo "Rebuilding and restarting containers..."
docker compose -f docker-compose.prod.yml up -d --build 2>> "$LOGFILE"

echo "Site redeployed successfully!"
