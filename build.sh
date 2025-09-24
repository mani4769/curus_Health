#!/bin/bash
# Build script for deployment

echo "🚀 Building Project Management Tool for deployment..."

# Build frontend
echo "📦 Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build complete!"
echo "📤 Ready for deployment to Railway/Render/Heroku"
echo ""
echo "Next steps:"
echo "1. Push to GitHub"
echo "2. Deploy to Railway (recommended): https://railway.app"
echo "3. Set environment variables in Railway:"
echo "   - GROQ_API_KEY=your-api-key"
echo "   - MONGODB_URI=will-be-provided-by-railway"
echo "   - JWT_SECRET_KEY=your-secret-key"
echo "   - DATABASE_NAME=project_management_db"
