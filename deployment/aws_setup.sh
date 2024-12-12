#!/bin/bash

# AWS EC2 Instance Configuration
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS in us-east-1
KEY_NAME="ecommerce-key"
SECURITY_GROUP_NAME="ecommerce-sg"

# Create Security Group
echo "Creating security group..."
aws ec2 create-security-group \
    --group-name $SECURITY_GROUP_NAME \
    --description "Security group for ecommerce application"

# Configure Security Group Rules
echo "Configuring security group rules..."
aws ec2 authorize-security-group-ingress \
    --group-name $SECURITY_GROUP_NAME \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name $SECURITY_GROUP_NAME \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name $SECURITY_GROUP_NAME \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Create Key Pair
echo "Creating key pair..."
aws ec2 create-key-pair \
    --key-name $KEY_NAME \
    --query 'KeyMaterial' \
    --output text > ${KEY_NAME}.pem

chmod 400 ${KEY_NAME}.pem

# Launch EC2 Instance
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-groups $SECURITY_GROUP_NAME \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get Public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "EC2 instance is ready!"
echo "Instance ID: $INSTANCE_ID"
echo "Public IP: $PUBLIC_IP"
echo "SSH Key: ${KEY_NAME}.pem"

# Create .env file with EC2 details
echo "Creating .env file..."
cat > ../.env << EOL
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///ecommerce.db
ADMIN_EMAIL=admin@example.com

# AWS Configuration
AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
AWS_REGION=$AWS_DEFAULT_REGION
EC2_INSTANCE_IP=$PUBLIC_IP
EOL

echo "Setup complete! Use these details to configure your GitHub Actions secrets." 