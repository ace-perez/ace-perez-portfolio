#!/bin/bash
cd /home/ec2-user/ace-perez-portfolio
source .venv/bin/activate
exec gunicorn --workers 3 --bind 127.0.0.1:5001 app:app
