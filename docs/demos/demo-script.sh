#!/bin/bash
# Demo Script for docker-microservices-template
#
# This script provides commands to demonstrate the project for screen recording.
# Use a tool like asciinema, OBS, or QuickTime to record, then convert to GIF with gifski.
#
# Recommended recording settings:
# - Terminal: 120x30 characters
# - Font size: 14-16pt
# - Theme: Dark background with good contrast
# - Duration target: 30-60 seconds

set -e

echo "=== Docker Microservices Template Demo ==="
echo ""

# Step 1: Show project structure
echo "📁 Project Structure:"
tree -L 2 --dirsfirst -I 'node_modules|__pycache__|.git|venv' . 2>/dev/null || ls -la

sleep 2

# Step 2: Start services
echo ""
echo "🚀 Starting all services with Docker Compose..."
docker-compose up -d

sleep 3

# Step 3: Check running containers
echo ""
echo "📦 Running containers:"
docker-compose ps

sleep 2

# Step 4: Test API endpoint
echo ""
echo "🔍 Testing API endpoints..."
echo ""
echo "GET /api/health:"
curl -s http://localhost:8000/api/health | jq .

sleep 1

echo ""
echo "GET /api/items:"
curl -s http://localhost:8000/api/items | jq .

sleep 2

# Step 5: Show Grafana dashboard
echo ""
echo "📊 Grafana available at: http://localhost:3001"
echo "   Default credentials: admin/admin"

sleep 1

# Step 6: Show metrics
echo ""
echo "📈 Prometheus metrics endpoint:"
curl -s http://localhost:8000/metrics | head -20

sleep 2

# Step 7: Cleanup (optional - comment out for continuous demo)
# echo ""
# echo "🧹 Cleaning up..."
# docker-compose down

echo ""
echo "✅ Demo complete! Services are running."
echo ""
echo "Available endpoints:"
echo "  - Frontend: http://localhost:3000"
echo "  - API:      http://localhost:8000"
echo "  - Grafana:  http://localhost:3001"
echo "  - Prometheus: http://localhost:9090"
