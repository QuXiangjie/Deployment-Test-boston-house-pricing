#!/bin/bash

# Test script to verify deployment consistency
echo "🧪 Testing deployment consistency..."

# Check if required files exist
echo "📁 Checking required files..."
required_files=("Dockerfile" "requirements.txt" "app_fastapi.py" "regmodel.pkl" "scaling.pkl" "deploy_ec2.sh")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Check Docker image name consistency
echo -e "\n🐳 Checking Docker configuration..."
if grep -q "california-housing-api" Dockerfile; then
    echo "✅ Dockerfile uses consistent naming"
else
    echo "⚠️  Dockerfile naming may be inconsistent"
fi

if grep -q "california-housing-api" deploy_ec2.sh; then
    echo "✅ Deploy script uses consistent naming"
else
    echo "⚠️  Deploy script naming may be inconsistent"
fi

if grep -q "california-housing-api" docker-compose.yml; then
    echo "✅ Docker Compose uses consistent naming"
else
    echo "⚠️  Docker Compose naming may be inconsistent"
fi

# Check port consistency
echo -e "\n🌐 Checking port configuration..."
if grep -q "EXPOSE 8000" Dockerfile && grep -q "80:8000" deploy_ec2.sh; then
    echo "✅ Port mapping is consistent (External: 80, Internal: 8000)"
else
    echo "⚠️  Port mapping may be inconsistent"
fi

echo -e "\n✅ Consistency check completed!"
echo "💡 Run this before deployment to ensure everything is aligned."
