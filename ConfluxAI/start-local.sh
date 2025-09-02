#!/bin/bash

echo "🚀 Starting Task-Automator Pro Local Development Server"
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "📝 Creating .env.local from template..."
    cp .env.local.example .env.local
    echo "✅ .env.local created. Please review and update if needed."
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed."
else
    echo "✅ Dependencies already installed."
fi

# Build frontend if dist doesn't exist
if [ ! -d "client/dist" ]; then
    echo "🔨 Building frontend..."
    npm run build
    echo "✅ Frontend built."
else
    echo "✅ Frontend already built."
fi

echo ""
echo "🌐 Starting development server..."
echo "📱 Frontend will be available at: http://localhost:5000"
echo "🔌 API will be available at: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev:vercel
