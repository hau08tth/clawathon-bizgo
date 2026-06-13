#!/bin/bash
set -e

echo "🚀 Starting BizGro Platform..."

# Check .env exists
if [ ! -f ".env" ]; then
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please add your ANTHROPIC_API_KEY to .env"
    exit 1
fi

# Check OPENAI_API_KEY
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  OPENAI_API_KEY not set in .env"
    echo "Please add: OPENAI_API_KEY=sk-..."
fi

echo "🐳 Starting Docker services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ BizGro is running!"
echo ""
echo "  🌐 Frontend:  http://localhost:3000"
echo "  🔧 API:       http://localhost:8000"
echo "  📖 API Docs:  http://localhost:8000/docs"
echo "  🚪 Gateway:   http://localhost:80"
echo ""
echo "  Demo login:"
echo "  📧 demo@zalopay.vn / demo123"
echo "  👑 admin@zalopay.vn / admin123"
echo ""
