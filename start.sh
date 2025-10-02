#!/bin/bash

# Start script for Render deployment
echo "🚀 Starting Enfue Search Demo on Render"

# Setup Typesense data if not already done
if [ ! -f "data_imported" ]; then
    echo "📊 Setting up Typesense data..."
    python setup_typesense.py
    if [ $? -eq 0 ]; then
        touch data_imported
        echo "✅ Data import completed"
    else
        echo "⚠️ Data import failed, continuing anyway..."
    fi
fi

# Start the web server
echo "🌐 Starting web server on port $PORT..."
python serve_demo_docker.py
