#!/bin/bash
# Deployment helper — pushes to your Vercel + Render projects
set -e
echo "🚀 Deploying DiligenceAI..."
git push origin main
echo "✅ Vercel + Render will auto-deploy from GitHub"
