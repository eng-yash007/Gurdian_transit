#!/usr/bin/env bash
# Development startup helper script for Guardian Transit AI

set -e

echo "=========================================="
echo "🛡️ Starting Guardian Transit AI (Local Dev)"
echo "=========================================="

if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH."
    exit 1
fi

if [ ! -f .env ]; then
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
fi

echo "🚀 Building and spinning up containers with Docker Compose..."
docker compose up --build -d

echo ""
echo "✅ Guardian Transit AI Services started successfully!"
echo "------------------------------------------------------"
echo "🌐 Frontend:             http://localhost:3000"
echo "⚡ Backend API:          http://localhost:8000"
echo "📑 Swagger API Docs:     http://localhost:8000/docs"
echo "🩺 Health Check:         http://localhost:8000/api/v1/health"
echo "🐘 PostgreSQL Database:  localhost:5432"
echo "------------------------------------------------------"
echo "View logs with: docker compose logs -f"
