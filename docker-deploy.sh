#!/bin/bash

# Fixed Docker setup for Enfue Search Demo
echo "🐳 Fixed Docker Setup for Enfue Search Demo"
echo "============================================="

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker stop enfue-typesense enfue-web 2>/dev/null || true
docker rm enfue-typesense enfue-web 2>/dev/null || true

# Pull required images first
echo "📥 Pulling required Docker images..."
docker pull python:3.11-slim
docker pull typesense/typesense:29.0

if [ $? -ne 0 ]; then
    echo "❌ Failed to pull Docker images"
    echo "💡 Try: docker login"
    exit 1
fi

echo "✅ Docker images pulled successfully"

# Start Typesense
echo "🚀 Starting Typesense..."
docker run -d \
  --name enfue-typesense \
  -p 8108:8108 \
  -v enfue-typesense-data:/data \
  typesense/typesense:29.0 \
  --data-dir /data \
  --api-key=Hu52dwsas2AdxdE \
  --listen-port 8108 \
  --enable-cors

if [ $? -eq 0 ]; then
    echo "✅ Typesense started successfully"
else
    echo "❌ Failed to start Typesense"
    exit 1
fi

# Wait for Typesense to be ready
echo "⏳ Waiting for Typesense to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8108/health > /dev/null 2>&1; then
        echo "✅ Typesense is ready"
        break
    fi
    echo -n "."
    sleep 2
done

# Start web service with better error handling
echo "🌐 Starting web service..."
docker run -d \
  --name enfue-web \
  -p 8080:8080 \
  --link enfue-typesense:typesense \
  -v "$(pwd)/index.html:/app/index.html:ro" \
  -v "$(pwd)/advanced-search.html:/app/advanced-search.html:ro" \
  -v "$(pwd)/semantic-search.html:/app/semantic-search.html:ro" \
  -v "$(pwd)/setup_typesense.py:/app/setup_typesense.py:ro" \
  -v "$(pwd)/semantic_natural_demo.py:/app/semantic_natural_demo.py:ro" \
  -v "$(pwd)/serve_demo_docker.py:/app/serve_demo_docker.py:ro" \
  -v "$(pwd)/Run_Browser_Agent_With_A_Goal_In_Background_2025-10-02T03_02_40.209Z.csv:/app/Run_Browser_Agent_With_A_Goal_In_Background_2025-10-02T03_02_40.209Z.csv:ro" \
  -w /app \
  python:3.11-slim \
  bash -c "
    echo 'Installing system dependencies...' &&
    apt-get update -qq &&
    apt-get install -y -qq curl jq &&
    echo 'Installing Python dependencies...' &&
    pip install --no-cache-dir typesense requests &&
    echo 'Setting up data...' &&
    python setup_typesense.py &&
    echo 'Starting web server...' &&
    python serve_demo_docker.py
  "

if [ $? -eq 0 ]; then
    echo "✅ Web service started successfully"
else
    echo "❌ Failed to start web service"
    echo "📊 Checking logs..."
    docker logs enfue-web
    exit 1
fi

# Wait for web service to be ready
echo "⏳ Waiting for web service to be ready..."
for i in {1..60}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Web service is ready"
        break
    fi
    echo -n "."
    sleep 2
done

# Check if web service is actually running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "⚠️ Web service may not be ready yet"
    echo "📊 Checking logs..."
    docker logs enfue-web --tail 20
fi

echo ""
echo "🎉 Enfue Search Demo is running!"
echo ""
echo "📋 Access URLs:"
echo "  🌐 Main Demo: http://localhost:8080/index.html"
echo "  🔍 Advanced Search: http://localhost:8080/advanced-search.html"
echo "  🧠 Semantic Search: http://localhost:8080/semantic-search.html"
echo "  🔧 Typesense API: http://localhost:8108"
echo ""
echo "🛠️ Management Commands:"
echo "  📊 View logs: docker logs enfue-web"
echo "  🛑 Stop: docker stop enfue-typesense enfue-web"
echo "  🗑️ Remove: docker rm enfue-typesense enfue-web"
echo "  🧹 Clean data: docker volume rm enfue-typesense-data"
echo ""
echo "🔍 Troubleshooting:"
echo "  If web service fails, check: docker logs enfue-web"
echo "  If Typesense fails, check: docker logs enfue-typesense"
echo "  To restart: docker restart enfue-web"
