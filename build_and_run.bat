@echo off
echo Building React frontend...
cd frontend
npm install
npm run build
echo Frontend build complete!
cd ..
echo Starting Flask server...
python backend/app.py
