#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx

# Create application directory
mkdir -p /home/ubuntu/ecommerce-app
cd /home/ubuntu/ecommerce-app

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Copy systemd service file
sudo cp deployment/ecommerce.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ecommerce
sudo systemctl start ecommerce

# Configure Nginx
sudo cp deployment/nginx.conf /etc/nginx/sites-available/ecommerce
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# Set up SSL (optional)
# sudo apt-get install -y certbot python3-certbot-nginx
# sudo certbot --nginx -d your_domain.com

# Set up firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

echo "Deployment completed successfully!" 