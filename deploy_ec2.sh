#!/bin/bash

# AWS EC2 Docker Deployment Script
# Run this on your EC2 instance

echo "🚀 Starting AWS EC2 Docker Deployment..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "📦 Installing Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose (optional but useful)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "⬇️ Downloading your application..."
# Option 1: If you have the files locally, upload them first
# Option 2: Clone from GitHub (recommended)
# git clone https://github.com/yourusername/california-housing-api.git
# cd california-housing-api

# For now, assuming files are already uploaded to EC2 in ~/california-housing-api/
echo "🐳 Building Docker image..."
sudo docker build -t california-housing-api .

echo "🚀 Running the container..."
# Stop any existing container
sudo docker stop california-housing-api 2>/dev/null || true
sudo docker rm california-housing-api 2>/dev/null || true

# Run the new container
sudo docker run -d \
  --name california-housing-api \
  --restart unless-stopped \
  -p 80:8000 \
  california-housing-api

# Check if container is running
echo "✅ Checking container status..."
sudo docker ps

# Show the public IP
echo "🌐 Your API is available at:"
echo "http://$(curl -s ifconfig.me)/"
echo "http://$(curl -s ifconfig.me)/docs"
echo "http://$(curl -s ifconfig.me)/health"

echo "✅ Deployment completed!"

# Optional: Setup SSL with Let's Encrypt
echo "💡 To add SSL (HTTPS), run: sudo certbot --nginx"
