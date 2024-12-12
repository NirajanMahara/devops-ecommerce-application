#!/bin/bash

# Update system packages
sudo yum update -y

# Install Nginx using amazon-linux-extras
sudo amazon-linux-extras install nginx1 -y

# Install Python 3.9 and development tools
sudo yum groupinstall "Development Tools" -y
sudo yum install python39 python39-devel -y

# Create virtual environment with Python 3.9
python3.9 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install 'Flask<3.0.0'  # Use Flask 2.x for Python 3.7 compatibility
pip install -r requirements.txt
pip install gunicorn

# Create necessary directories
sudo mkdir -p /etc/nginx/conf.d/

# Copy systemd service file
sudo cp deployment/ecommerce.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ecommerce
sudo systemctl restart ecommerce

# Configure Nginx
sudo cp deployment/nginx.conf /etc/nginx/conf.d/ecommerce.conf
sudo systemctl enable nginx
sudo systemctl restart nginx

# Set proper permissions
sudo chown -R ec2-user:ec2-user /home/ec2-user/ecommerce-app

echo "Deployment completed successfully!" 