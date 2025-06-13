# 🐳 Docker + AWS EC2 Deployment Guide

## Prerequisites
- AWS Account
- Key pair (.pem file) for EC2 access
- Docker installed locally (for testing)

## Important: Consistent Naming Convention
This guide uses **consistent naming** throughout:
- **Container name**: `california-housing-api`
- **Image name**: `california-housing-api`
- **Project folder**: `california-housing-api`
- **External port**: `80` (mapped to internal port `8000`)

## Step 1: Build and Test Locally

```bash
# Build Docker image
docker build -t california-housing-api .

# Test locally
docker run -p 8000:8000 california-housing-api

# Test the API
curl http://localhost:8000/health
```

## Step 2: Launch AWS EC2 Instance

### EC2 Configuration:
- **AMI**: Ubuntu 22.04 LTS
- **Instance Type**: t2.micro (free tier) or t2.small
- **Key Pair**: Your existing key pair
- **Security Group**: 
  - SSH (22) - Your IP only
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0
  - Custom TCP (8000) - 0.0.0.0/0 (for testing)

## Step 3: Upload Files to EC2

```bash
# Upload your project files
scp -i your-key.pem -r . ubuntu@your-ec2-ip:~/california-housing-api/

# Or clone from GitHub (recommended)
# ssh -i your-key.pem ubuntu@your-ec2-ip
# git clone https://github.com/yourusername/california-housing-api.git
```

## Step 4: Deploy with Docker

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# Navigate to project
cd california-housing-api

# Make deployment script executable
chmod +x deploy_ec2.sh

# Run deployment
./deploy_ec2.sh
```

## Step 5: Alternative - Using Docker Compose

```bash
# Simple deployment
docker-compose up -d

# With nginx (for production)
docker-compose --profile nginx up -d

# View logs
docker-compose logs -f

# Update deployment
docker-compose pull && docker-compose up -d
```

## Step 6: Test Your Deployed API

```bash
# Replace YOUR_EC2_IP with your actual IP
curl http://YOUR_EC2_IP/health
curl http://YOUR_EC2_IP/docs

# Test Power BI endpoints
curl -X POST http://YOUR_EC2_IP/powerbi/predict \
  -H "Content-Type: application/json" \
  -d '{
    "MedInc": 3.5673,
    "HouseAge": 11.0,
    "AveRooms": 5.93,
    "AveBedrms": 1.13,
    "Population": 1257.0,
    "AveOccup": 2.82,
    "Latitude": 39.29,
    "Longitude": -121.32
  }'
```

## Step 7: Power BI Integration

Use these URLs in Power BI:
- **Health Check**: `http://YOUR_EC2_IP/health`
- **Sample Data**: `http://YOUR_EC2_IP/powerbi/sample-data`
- **Single Predict**: `http://YOUR_EC2_IP/powerbi/predict`
- **Bulk Predict**: `http://YOUR_EC2_IP/powerbi/bulk-predict`
- **Interactive Docs**: `http://YOUR_EC2_IP/docs`
- **Test Page**: `http://YOUR_EC2_IP/test`

## Benefits of This Docker Approach:

✅ **Consistent Environment**: Works same everywhere
✅ **Easy Updates**: `docker-compose pull && docker-compose up -d`
✅ **Easy Scaling**: Add more containers or instances
✅ **Isolation**: App runs in contained environment
✅ **Rollback**: Easy to revert to previous versions
✅ **Monitoring**: Built-in health checks

## Production Enhancements:

1. **SSL Certificate**: Add Let's Encrypt
2. **Domain Name**: Use Route53
3. **Load Balancer**: AWS Application Load Balancer
4. **Auto Scaling**: EC2 Auto Scaling Groups
5. **Database**: RDS for data storage
6. **Monitoring**: CloudWatch + Docker logs

## Estimated Costs:

- **t2.micro**: FREE (first 12 months)
- **t2.small**: ~$17/month
- **Domain**: ~$12/year
- **Load Balancer**: ~$18/month (only if needed)

## Quick Commands:

```bash
# View running containers
docker ps

# View logs
docker logs california-housing-api

# Update application
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Backup
docker save california-housing-api > housing-api-backup.tar
```
