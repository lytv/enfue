#!/bin/bash

# Simple Local Setup (No Docker credentials needed)
echo "🚀 Simple Local Setup for Enfue Search Demo"
echo "============================================="

# Check if Typesense is running
if ! curl -s http://localhost:8108/health > /dev/null 2>&1; then
    echo "❌ Typesense is not running"
    echo "💡 Please start Typesense first:"
    echo "   docker run -d --name enfue-typesense -p 8108:8108 -v/tmp/data:/data typesense/typesense:29.0 --data-dir /data --api-key=Hu52dwsas2AdxdE"
    exit 1
fi

echo "✅ Typesense is running"

# Check if Python dependencies are installed
if ! python3 -c "import typesense" 2>/dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install typesense requests
fi

echo "✅ Python dependencies ready"

# Setup data if not already done
echo "📊 Setting up data..."
python3 setup_typesense.py

if [ $? -eq 0 ]; then
    echo "✅ Data setup completed"
else
    echo "⚠️ Data setup failed, but continuing..."
fi

# Start web server
echo "🌐 Starting web server..."
echo "🎉 Demo is now running!"
echo ""
echo "📋 Access URLs:"
echo "  🌐 Main Demo: http://localhost:8080/index.html"
echo "  🔍 Advanced Search: http://localhost:8080/advanced-search.html"
echo "  🧠 Semantic Search: http://localhost:8080/semantic-search.html"
echo "  🔧 Typesense API: http://localhost:8108"
echo ""
echo "🛑 Press Ctrl+C to stop the server"

python3 serve_demo.py
