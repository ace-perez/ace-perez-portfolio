#!/bin/bash

LOGDIR="$HOME/ace-perez-portfolio/errors"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/$(date +'%Y-%m-%d_%H-%M-%S').log"

echo "Going to project directory..."
cd ~/ace-perez-portfolio || exit 1

echo "Pulling latest code from GitHub..."
git fetch && git reset origin/main --hard

echo "Creating nginx config directory and file..."
mkdir -p user_conf.d

# Create the nginx config with correct domain
cat > user_conf.d/myportfolio.conf << 'EOF'
server {
    listen 80;
    server_name ace-perez-portfolio.dev;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name ace-perez-portfolio.dev;

    ssl_certificate /etc/letsencrypt/live/ace-perez-portfolio.dev/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ace-perez-portfolio.dev/privkey.pem;

    location / {
        proxy_pass http://myportfolio:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
}
EOF

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
echo "Visit: https://ace-perez-portfolio.dev"