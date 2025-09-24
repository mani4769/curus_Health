#!/bin/bash
# Fix permissions and run build
echo "Fixing permissions..."
chmod +x ./node_modules/.bin/react-scripts
echo "Running build..."
npm run build
