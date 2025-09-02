# 🚀 Task-Automator Pro - Deployment Guide

This guide covers both **Vercel deployment** and **local development setup** for your Task-Automator project.

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Node.js 18+ installed
- ✅ npm or yarn package manager
- ✅ Git repository set up
- ✅ Vercel account (free tier is sufficient)
- ✅ Access to your n8n instance at `kasimlohar.app.n8n.cloud`

## 🏠 Local Development Setup

### Step 1: Install Dependencies
```bash
cd dynamic-task-automator-pro
npm install
```

### Step 2: Environment Configuration
```bash
# Copy the example environment file
cp .env.local.example .env.local

# Edit .env.local with your actual n8n webhook URLs
# The example file already contains the correct URLs
```

### Step 3: Build Frontend
```bash
# Build the React frontend
npm run build
```

### Step 4: Start Development Server
```bash
# Start the development server (handles both API and frontend)
npm run dev:vercel
```

Your local development server will be available at:
- 🌐 **Frontend**: http://localhost:5000
- 🔌 **API**: http://localhost:5000/api
- 🔄 **n8n Webhook**: http://localhost:5000/api/webhook/n8n
- 📄 **PDF Upload**: http://localhost:5000/api/upload-pdf
- 🖼️ **Image Upload**: http://localhost:5000/api/upload-image
- 🎬 **Video Upload**: http://localhost:5000/api/upload-video
- 🎵 **Audio Upload**: http://localhost:5000/api/upload-audio

## 🚀 Vercel Deployment

### Step 1: Prepare Your Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Deploy to Vercel

#### Option A: Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure the following settings:

**Build Settings:**
- **Framework Preset**: Other
- **Root Directory**: `./` (leave as default)
- **Build Command**: `npm run build`
- **Output Directory**: `client/dist`
- **Install Command**: `npm install`

**Environment Variables:**
Add these environment variables in your Vercel project settings:

```bash
# Application Environment
NODE_ENV=production

# n8n Webhook URLs (Production)
N8N_PDF_WEBHOOK_URL=https://kasimlohar.app.n8n.cloud/webhook/pdf-ingest
N8N_IMAGE_WEBHOOK_URL=https://kasimlohar.app.n8n.cloud/webhook/image-ingest
N8N_VIDEO_WEBHOOK_URL=https://kasimlohar.app.n8n.cloud/webhook/9cb9c3ff-f43f-4579-b21b-30dafc30c87b
N8N_AUDIO_WEBHOOK_URL=https://kasimlohar.app.n8n.cloud/webhook/2bb25d11-1ed8-4299-9ef4-f5bf091c3695
N8N_CHAT_WEBHOOK_URL=https://kasimlohar.app.n8n.cloud/webhook/bdd9a358-e97e-4da2-8aed-6fd474dec5a7

# n8n Webhook URLs (Test)
N8N_PDF_WEBHOOK_TEST_URL=https://kasimlohar.app.n8n.cloud/webhook-test/pdf-ingest
N8N_IMAGE_WEBHOOK_TEST_URL=https://kasimlohar.app.n8n.cloud/webhook-test/image-ingest
N8N_VIDEO_WEBHOOK_TEST_URL=https://kasimlohar.app.n8n.cloud/webhook-test/9cb9c3ff-f43f-4579-b21b-30dafc30c87b
N8N_AUDIO_WEBHOOK_TEST_URL=https://kasimlohar.app.n8n.cloud/webhook-test/2bb25d11-1ed8-4299-9ef4-f5bf091c3695
N8N_CHAT_WEBHOOK_TEST_URL=https://kasimlohar.app.n8n.cloud/webhook-test/bdd9a358-e97e-4da2-8aed-6fd474dec5a7
```

5. Click "Deploy"

#### Option B: Vercel CLI
```bash
# Install Vercel CLI globally
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# Follow the prompts to configure your project
```

### Step 3: Verify Deployment
After successful deployment:
1. Visit your Vercel deployment URL
2. Test all functionality:
   - ✅ Chat interface
   - ✅ PDF uploads
   - ✅ Image uploads
   - ✅ Video uploads
   - ✅ Audio uploads
   - ✅ Documents dashboard

## 🔧 Development Workflow

### Local Development
```bash
# Start development server (handles both API and frontend)
npm run dev:vercel

# In another terminal, watch for frontend changes
npm run build -- --watch
```

### Production Build
```bash
# Build for production
npm run build

# The build output goes to client/dist/
```

### Testing API Routes Locally
```bash
# Test n8n webhook proxy
curl -X POST http://localhost:5000/api/webhook/n8n \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","webhookUrl":"https://kasimlohar.app.n8n.cloud/webhook-test/bdd9a358-e97e-4da2-8aed-6fd474dec5a7"}'

# Test PDF upload
curl -X POST http://localhost:5000/api/upload-pdf \
  -F "file=@test.pdf" \
  -F "webhookUrl=https://kasimlohar.app.n8n.cloud/webhook-test/pdf-ingest"
```

## 🐛 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check TypeScript compilation
npm run check
```

#### API Route Issues
- Ensure all API routes are in the `api/` directory
- Check that file names match the route paths
- Verify environment variables are set correctly

#### Frontend Build Issues
```bash
# Clear build cache
rm -rf client/dist

# Rebuild frontend
npm run build
```

### Debug Commands
```bash
# Check deployment logs (Vercel)
vercel logs [deployment-url]

# Test database connection locally
npm run check

# Build locally to test
npm run build

# Test production build locally
npm run start:vercel
```

## 📁 Project Structure

```
dynamic-task-automator-pro/
├── api/                          # Vercel serverless functions
│   ├── webhook/n8n.ts           # n8n webhook proxy
│   ├── upload-pdf.ts            # PDF upload handler
│   ├── upload-image.ts          # Image upload handler
│   ├── upload-video.ts          # Video upload handler
│   ├── upload-audio.ts          # Audio upload handler
│   └── dev-server.ts            # Local development server
├── client/                       # React frontend
│   ├── src/                     # Source code
│   └── dist/                    # Build output
├── server/                       # Original Express server (for reference)
├── vercel.json                  # Vercel configuration
├── package.json                 # Dependencies and scripts
├── .env.local.example           # Environment variables template
└── DEPLOYMENT.md                # This file
```

## 🔄 Continuous Deployment

Once deployed to Vercel:
- Every push to your `main` branch will trigger automatic deployment
- Vercel will build and deploy your changes automatically
- You can preview deployments on feature branches

## 📞 Support

If you encounter issues:
1. Check the Vercel deployment logs
2. Verify environment variables are set correctly
3. Test locally first using `npm run dev:vercel`
4. Check that all n8n webhook URLs are accessible

## 🎯 Next Steps

After successful deployment:
1. Test all functionality on the live site
2. Set up custom domain if needed
3. Configure monitoring and analytics
4. Set up staging environment for testing
5. Document any additional configuration needed

---

**Happy Deploying! 🚀**
