#!/bin/bash

# Update system packages
sudo yum update -y

# Install required packages
sudo yum install -y python3-pip nginx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Copy systemd service file
sudo cp deployment/ecommerce.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ecommerce
sudo systemctl start ecommerce

# Configure Nginx
sudo cp deployment/nginx.conf /etc/nginx/conf.d/ecommerce.conf
sudo systemctl restart nginx

echo "Deployment completed successfully!" 