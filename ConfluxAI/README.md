# 🤖 ConfluxAI - AI-Powered Multi-Media Knowledge Base

## 📋 Table of Contents
<div align="center">

![ConfluxAI Banner](https://img.shields.io/badge/ConfluxAI-Multi--Media%20Knowledge%20Base-blue?style=for-the-badge&logo=artificial-intelligence)

[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=flat&logo=react)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.3-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=flat&logo=node.js)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/Express-4.21.2-000000?style=flat&logo=express)](https://expressjs.com/)
[![Vite](https://img.shields.io/badge/Vite-5.4.14-646CFF?style=flat&logo=vite)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4.17-06B6D4?style=flat&logo=tailwind-css)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/kasimlohar/kurukshetra?style=social)](https://github.com/kasimlohar/kurukshetra/stargazers)

*An intelligent multi-media knowledge base that processes documents, images, videos, and audio files using AI workflows powered by n8n automation.*

[🚀 Live Demo](https://conflux-ai.vercel.app) • [✨ Features](#features) • [🛠️ Installation](#installation) • [📖 Usage](#usage) • [🔧 Configuration](#configuration) • [🤝 Contributing](#contributing)

**⭐ If you find this project helpful, please consider giving it a star!**

</div>

## � Screenshots

<div align="center">

### 🏠 Main Interface
*Modern glassmorphism design with intuitive navigation*

<img src="docs/screenshots/main-interface.png" alt="ConfluxAI Main Interface" width="800" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">

---

### 💬 AI Chat Interface
*Intelligent conversation with your uploaded content*

<img src="docs/screenshots/chat-interface.png" alt="AI Chat Interface" width="800" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">

---

### 📤 File Upload System
*Drag & drop multi-media file processing*

<img src="docs/screenshots/file-upload.png" alt="File Upload System" width="800" style="border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">

</div>

## �📋 Table of Contents

- [Screenshots](#-screenshots)
- [Features](#-features)
- [Architecture](#️-architecture)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Development](#️-development)

## ✨ Features

### 🧠 **AI-Powered Processing**
- 🤖 **Intelligent Document Analysis**: Extract and analyze content from PDFs with AI
- 👁️ **Image Recognition**: Process and understand visual content using advanced AI models  
- 🎬 **Video Intelligence**: Extract insights and transcripts from video files
- 🎵 **Audio Processing**: Transcribe and analyze audio content with speech-to-text
- 💬 **Smart Chat Interface**: Conversational AI that can query and understand processed content
- 🔍 **Semantic Search**: Find relevant information across all your uploaded files
- 🧠 **Context-Aware Responses**: AI maintains conversation context and provides relevant answers

### 🎨 **Modern UI & Experience**
- 🌈 **Glassmorphism Design**: Beautiful glass-effect components with backdrop blur
- 🌙 **Smart Theme System**: Auto-detects system preferences with manual override (light/dark/system)
- 🎭 **Smooth Animations**: Framer Motion powered micro-interactions respecting accessibility
- ⌨️ **Full Keyboard Navigation**: Complete keyboard accessibility with proper ARIA support
- 📱 **Responsive Design**: Optimized for all screen sizes from mobile to desktop
- 🚀 **Performance Optimized**: Lazy loading, code splitting, and optimized bundle sizes
- ♿ **WCAG AA Compliant**: Color contrast, focus management, and screen reader support

### 📁 **Multi-Media Support**
- 📄 **PDF Documents** (.pdf - up to 10MB)
- 🖼️ **Images** (.jpg, .png, .gif, .webp - up to 10MB)
- 🎬 **Videos** (.mp4, .avi, .mov, .webm - up to 100MB)
- 🎵 **Audio** (.mp3, .wav, .ogg, .m4a - up to 50MB)

### 🎨 **Modern UI/UX**
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- 🌓 **Dark/Light Themes**: User preference-based theming with system detection
- 🎯 **Drag & Drop**: Intuitive file upload experience with visual feedback
- ⚡ **Real-time Progress**: Live upload and processing status with progress bars
- 📊 **Interactive Dashboard**: Organized document management with search and filters
- ♿ **Accessibility**: Full keyboard navigation and screen reader support

### 🔧 **Technical Features**
- 🔄 **n8n Workflow Integration**: Automated processing pipelines with visual workflow editor
- 🔐 **Authentication System**: Secure user management with session-based auth
- 📡 **Real-time Updates**: WebSocket-based live updates for processing status
- 🛡️ **Error Handling**: Comprehensive error management with user-friendly messages
- 🔒 **Type Safety**: Full TypeScript implementation for better code quality
- ⚡ **Performance Optimized**: Lazy loading, code splitting, and caching strategies
- 🐳 **Docker Ready**: Containerized deployment support
- 🔄 **CI/CD Ready**: GitHub Actions workflows included

## 🏗️ Architecture

<div align="center">

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React + TypeScript + Vite]
        B[Tailwind CSS + shadcn/ui]
        C[React Router + Query]
    end
    
    subgraph "Backend Layer"
        D[Express.js Server]
        E[Vercel Functions]
        F[Authentication Layer]
    end
    
    subgraph "AI Processing Layer"
        G[n8n Workflows]
        H[Google Gemini API]
        I[Vector Database]
    end
    
    subgraph "Data Layer"
        J[PostgreSQL/SQLite]
        K[File Storage]
        L[Session Store]
    end
    
    A --> D
    A --> E
    D --> F
    E --> F
    F --> G
    G --> H
    G --> I
    D --> J
    E --> J
    D --> K
    E --> K
    F --> L
```

</div>

### 📁 Project Structure

```
ConfluxAI/
├── 🎨 client/                 # React Frontend Application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── ui/           # Basic UI components (shadcn/ui)
│   │   │   ├── Auth/         # Authentication components
│   │   │   └── ...           # Feature-specific components
│   │   ├── pages/            # Application pages/routes
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utilities and helper functions
│   │   └── types/            # TypeScript type definitions
│   ├── public/               # Static assets (images, icons, etc.)
│   └── index.html            # Main HTML template
├── 🔧 api/                   # Vercel Serverless Functions
│   ├── webhook/              # n8n webhook handlers
│   │   └── n8n.ts           # Main webhook endpoint
│   ├── upload-pdf.ts         # PDF processing endpoint
│   ├── upload-image.ts       # Image processing endpoint
│   ├── upload-video.ts       # Video processing endpoint
│   ├── upload-audio.ts       # Audio processing endpoint
│   └── dev-server.ts         # Development server setup
├── 🖥️ server/               # Express.js Backend (Development)
│   ├── index.ts              # Main server entry point
│   ├── routes.ts             # API route definitions
│   ├── storage.ts            # File storage management
│   └── vite.ts               # Vite integration for SSR
├── 🤖 n8n_workflows/        # Automation Workflows
│   ├── AI agent.json         # Main AI processing workflow
│   ├── pdf_saving_func.json  # PDF processing workflow
│   ├── image processing.json # Image analysis workflow
│   ├── video processing.json # Video processing workflow
│   └── audio processing.json # Audio transcription workflow
├── 📋 shared/               # Shared utilities
│   └── schema.ts             # TypeScript type definitions
├── 🔧 Configuration Files
│   ├── package.json          # Dependencies and scripts
│   ├── tsconfig.json         # TypeScript configuration
│   ├── vite.config.ts        # Vite build configuration
│   ├── tailwind.config.ts    # Tailwind CSS configuration
│   ├── drizzle.config.ts     # Database ORM configuration
│   └── vercel.json           # Vercel deployment settings
└── 📚 Documentation
    ├── README.md             # Main project documentation
    ├── CONTRIBUTING.md       # Contribution guidelines
    ├── CHANGELOG.md          # Version history
    ├── DEPLOYMENT.md         # Deployment instructions
    └── .env.example          # Environment variables template
```

## 🚀 Quick Start

### 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **npm** or **yarn** package manager  
- **Git** for version control
- **n8n instance** (self-hosted or cloud) - [Setup Guide](https://docs.n8n.io/)
- **Google Gemini API key** (free tier available) - [Get API Key](https://ai.google.dev/)

### 1️⃣ Clone the Repository

```bash
# Clone the repository
git clone https://github.com/kasimlohar/kurukshetra.git

# Navigate to the ConfluxAI directory
cd kurukshetra/ConfluxAI

# Check Node.js version (should be 18+)
node --version
```

### 2️⃣ Install Dependencies

```bash
# Install all dependencies
npm install

# Verify installation
npm list --depth=0
```

### 3️⃣ Environment Setup

```bash
# Copy the environment template
cp .env.example .env

# Open .env file in your preferred editor
# Windows
notepad .env

# macOS/Linux
nano .env
# or
code .env
```

### 4️⃣ Configure Environment Variables

**Required Variables:**

Open `.env` file and update the following essential variables:

```bash
# ====== GOOGLE GEMINI API (FREE TIER) ======
# Get your free API key from: https://ai.google.dev/
GOOGLE_GEMINI_API_KEY=your_free_gemini_api_key_here

# ====== N8N WORKFLOW AUTOMATION ======  
# Your n8n instance URL (self-hosted or cloud)
N8N_BASE_URL=http://localhost:5678
N8N_WEBHOOK_AUTH=your_webhook_auth_token

# ====== DATABASE CONFIGURATION ======
# For development, you can use SQLite (no setup required)
DATABASE_URL=sqlite:./local.db
# For production, use PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/conflux_ai

# ====== AUTHENTICATION ======
SESSION_SECRET=your-super-secure-session-secret-here
```

**Optional Variables for Enhanced Features:**

```bash
# ====== VECTOR DATABASE (OPTIONAL) ======
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# ====== ADDITIONAL AI FEATURES (OPTIONAL) ======
OPENAI_API_KEY=your_openai_api_key  # For embeddings
SERP_API_KEY=your_serp_api_key      # For web search
```

### 5️⃣ Set up n8n Workflows

1. **Start your n8n instance**:
```bash
# If using Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n

# If installed globally
n8n start
```

2. **Import workflows**:
   - Open n8n interface (http://localhost:5678)
   - Go to Workflows → Import from File
   - Import all JSON files from `n8n_workflows/` directory
   - Configure your API keys in each workflow

3. **Update webhook URLs** in your `.env` file with the actual webhook URLs from n8n

### 6️⃣ Build and Start

```bash
# Build the application
npm run build

# Start development server with hot reload
npm run dev

# OR start with Vercel-compatible mode
npm run dev:vercel
```

### 7️⃣ Access the Application

Once the server starts successfully:

- 🌐 **Frontend**: http://localhost:5000
- 🔌 **API**: http://localhost:5000/api  
- 📄 **Upload Endpoints**: http://localhost:5000/api/upload-*
- 🤖 **n8n Interface**: http://localhost:5678

### 🚀 Verification

Test your setup by:

1. **Creating an account** at http://localhost:5000
2. **Uploading a test file** (try a small PDF first)
3. **Asking a question** in the chat interface about the uploaded file
4. **Checking n8n logs** to verify workflow execution

### 🔧 Troubleshooting

**Common issues:**

```bash
# Port already in use
npm run dev -- --port 3000

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check logs for errors
npm run dev 2>&1 | tee debug.log
```

**Need help?** Check our [Troubleshooting Guide](./TROUBLESHOOTING.md) or open an issue.

## 📖 Usage Guide

### 🔐 Authentication

1. **Sign Up**: Create a new account with email and password
2. **Login**: Access your personalized knowledge base
3. **Protected Routes**: All features require authentication

### 📤 File Upload

1. **Select File Type**: Choose from PDF, Image, Video, or Audio tabs
2. **Drag & Drop**: Drop files or click to browse
3. **Monitor Progress**: Watch real-time upload and processing status
4. **View Results**: Access processed content in the Documents dashboard

### 💬 Chat Interface

1. **Ask Questions**: Query your uploaded content using natural language
2. **Contextual Responses**: Get AI-powered answers based on your documents
3. **Multi-Modal**: Reference content from any uploaded file type
4. **Conversation History**: Previous chats are automatically saved

### 📊 Document Management

1. **Dashboard View**: See all uploaded and processed files
2. **Search & Filter**: Find specific documents quickly
3. **Status Tracking**: Monitor processing status and errors
4. **Metadata**: View file details, upload dates, and processing results

## 🔧 Configuration

### n8n Workflow Setup

1. **Import Workflows**: Import JSON files from `n8n_workflows/` to your n8n instance
2. **Configure Webhooks**: Update webhook URLs in your environment variables
3. **Set API Keys**: Configure Google Gemini API in n8n workflows
4. **Test Endpoints**: Verify all webhook endpoints are responding

### API Endpoints

| Endpoint | Method | Purpose | File Types |
|----------|--------|---------|------------|
| `/api/webhook/n8n` | POST | Chat processing | - |
| `/api/upload-pdf` | POST | PDF processing | .pdf |
| `/api/upload-image` | POST | Image analysis | .jpg, .png, .gif, .webp |
| `/api/upload-video` | POST | Video processing | .mp4, .avi, .mov, .webm |
| `/api/upload-audio` | POST | Audio transcription | .mp3, .wav, .ogg, .m4a |

### File Size Limits

- **PDFs**: 10MB maximum
- **Images**: 10MB maximum  
- **Videos**: 100MB maximum
- **Audio**: 50MB maximum

## 🚀 Deployment

### 🌟 Vercel Deployment (Recommended)

**Step-by-step deployment to Vercel:**

1. **Prepare your repository**:
```bash
# Ensure all changes are committed
git add .
git commit -m "feat: prepare for deployment"
git push origin main
```

2. **Deploy to Vercel**:
   - Visit [vercel.com](https://vercel.com) and sign in with GitHub
   - Click "New Project" and import your repository
   - Configure build settings:
     - **Framework Preset**: Other
     - **Build Command**: `npm run build:vercel`
     - **Output Directory**: `dist/public`
     - **Install Command**: `npm install`
     - **Node.js Version**: 18.x

3. **Environment Variables**:
   Add all required environment variables from `.env.example` in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add each variable from your `.env` file
   - ⚠️ **Important**: Use production URLs for webhooks and databases

4. **Custom Domain** (Optional):
   - Go to Project Settings → Domains
   - Add your custom domain
   - Configure DNS settings as instructed

### 🐳 Docker Deployment

**Create Dockerfile:**

```dockerfile
# Use official Node.js runtime as base image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Start application
CMD ["npm", "start"]
```

**Docker Compose setup:**

```yaml
version: '3.8'

services:
  conflux-ai:
    build: .
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      - postgres
      - n8n

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: conflux_ai
      POSTGRES_USER: conflux_user
      POSTGRES_PASSWORD: conflux_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  postgres_data:
  n8n_data:
```

**Deploy with Docker:**

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### ☁️ Cloud Platforms

#### **Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

#### **Render**
```bash
# Connect repository at render.com
# Set build command: npm run build
# Set start command: npm start
```

#### **DigitalOcean App Platform**
```yaml
# app.yaml
name: conflux-ai
services:
- name: web
  source_dir: /
  github:
    repo: kasimlohar/kurukshetra
    branch: main
  run_command: npm start
  build_command: npm run build
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
```

### 🔧 Production Checklist

Before deploying to production:

- [ ] **Environment Variables**: All required variables are set
- [ ] **Database**: Production database is configured and accessible
- [ ] **n8n Workflows**: All workflows are imported and tested
- [ ] **API Keys**: All API keys are valid and have sufficient quotas
- [ ] **Domain**: Custom domain is configured (if needed)
- [ ] **SSL**: HTTPS is enabled
- [ ] **Monitoring**: Error tracking and analytics are set up
- [ ] **Backups**: Database backup strategy is in place
- [ ] **Security**: Security headers and rate limiting are configured

### 📊 Monitoring & Analytics

**Recommended tools:**

- **Error Tracking**: [Sentry](https://sentry.io/)
- **Analytics**: [Google Analytics](https://analytics.google.com/)
- **Uptime Monitoring**: [UptimeRobot](https://uptimerobot.com/)
- **Performance**: [Vercel Analytics](https://vercel.com/analytics)

## 🛠️ Development

### Project Structure

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: Express.js + TypeScript for development, Vercel Functions for production
- **Database**: Drizzle ORM with PostgreSQL/SQLite support
- **Authentication**: Custom auth system with session management
- **AI Integration**: n8n workflows with Google Gemini API
- **Styling**: Tailwind CSS + shadcn/ui components

### Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Frontend** | React 18.3 | UI framework |
| **Language** | TypeScript 5.6 | Type safety |
| **Build Tool** | Vite 5.4 | Fast development and building |
| **Styling** | Tailwind CSS 3.4 | Utility-first CSS |
| **UI Components** | Radix UI + shadcn/ui | Accessible component library |
| **Backend** | Express.js 4.21 | Web framework |
| **Database ORM** | Drizzle 0.39 | Type-safe database queries |
| **Authentication** | Passport.js | Authentication middleware |
| **File Upload** | Multer 2.0 | Multipart form handling |
| **Automation** | n8n | Workflow automation |
| **AI** | Google Gemini | Language model |

### Available Scripts

```bash
# Development
npm run dev              # Start Express development server
npm run dev:vercel       # Start Vercel-compatible dev server

# Building
npm run build            # Build for production
npm run build:vercel     # Build for Vercel deployment

# Database
npm run db:push          # Push database schema changes

# Type Checking
npm run check            # TypeScript type checking
```

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or suggesting ideas, your help is appreciated.

### 🚀 Quick Contribution Guide

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **✨ Make your changes**: Follow our coding standards
4. **✅ Test your changes**: Ensure everything works correctly
5. **📝 Commit changes**: `git commit -m 'feat: add amazing feature'`
6. **🚀 Push to branch**: `git push origin feature/amazing-feature`  
7. **🔄 Open a Pull Request**: Describe your changes clearly

### 📋 Contribution Types

| Type | Description | Examples |
|------|-------------|----------|
| 🐛 **Bug Fixes** | Fix issues and problems | Error handling, UI bugs, API fixes |
| ✨ **New Features** | Add new functionality | New file types, AI models, UI components |
| 📚 **Documentation** | Improve docs and guides | README updates, API docs, tutorials |
| 🎨 **UI/UX Improvements** | Enhance user experience | Design improvements, accessibility |
| ⚡ **Performance** | Optimize speed and efficiency | Code optimization, caching, bundling |
| 🔒 **Security** | Security enhancements | Authentication, data validation |

### 💻 Development Guidelines

**Code Style:**
- Use **TypeScript** for all new code
- Follow **ESLint** and **Prettier** configurations
- Use **conventional commit** messages
- Add **JSDoc comments** for complex functions
- Maintain **test coverage** for new features

**Commit Convention:**
```bash
feat: add new feature
fix: resolve bug
docs: update documentation  
style: formatting changes
refactor: code restructuring
test: add or update tests
chore: maintenance tasks
```

**Before Submitting:**
- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] Changes are tested manually
- [ ] No console errors or warnings

### 🐛 Reporting Issues

**Bug Reports** should include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, Node.js version)

**Feature Requests** should include:
- Problem description
- Proposed solution
- Use cases and benefits
- Implementation ideas (optional)

### 📖 Development Resources

- **Style Guide**: [CONTRIBUTING.md](./CONTRIBUTING.md)
- **API Documentation**: [API.md](./docs/API.md)
- **Architecture Guide**: [ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

### 🙏 Recognition

Contributors are recognized in:
- README contributors section
- Release notes and changelogs
- Special mentions in major releases

### 💬 Getting Help

- **💬 Discussions**: [GitHub Discussions](https://github.com/kasimlohar/kurukshetra/discussions)
- **🐛 Issues**: [GitHub Issues](https://github.com/kasimlohar/kurukshetra/issues)
- **📧 Email**: kasimlohar@example.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Issues

- **Issues**: [GitHub Issues](https://github.com/kasimlohar/kurukshetra/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kasimlohar/kurukshetra/discussions)
- **Email**: kasimlohar@example.com

## 🙏 Acknowledgments

- **n8n Community** for excellent workflow automation
- **Google AI** for free Gemini API access
- **Vercel** for seamless deployment platform
- **Radix UI** for accessible component primitives
- **Tailwind CSS** for utility-first styling

## 🔮 Roadmap

### 🎯 Short Term (Q1 2025)

- [ ] **🔍 Enhanced Search**: Advanced semantic search with filters
- [ ] **📱 Mobile App**: React Native companion application
- [ ] **🔄 Batch Processing**: Multiple file upload and processing
- [ ] **📊 Analytics Dashboard**: Usage insights and metrics
- [ ] **🔐 Advanced Auth**: OAuth integration (Google, GitHub)
- [ ] **🌐 Multi-language**: Internationalization support

### 🚀 Medium Term (Q2-Q3 2025)

- [ ] **🤝 Real-time Collaboration**: Multi-user document editing
- [ ] **🔌 Plugin System**: Extensible workflow integrations  
- [ ] **🏢 Team Management**: Organization and role-based access
- [ ] **📈 Advanced Analytics**: Detailed usage and performance metrics
- [ ] **🔒 Enterprise Security**: SSO, audit logs, compliance features
- [ ] **💾 Version Control**: Document versioning and history

### 🌟 Long Term (Q4 2025+)

- [ ] **🧠 Custom AI Models**: Train domain-specific models
- [ ] **🔗 API Marketplace**: Third-party integrations marketplace
- [ ] **📱 Desktop Apps**: Native Windows, macOS, Linux applications
- [ ] **🌍 Edge Computing**: Distributed processing capabilities
- [ ] **🔮 Predictive Analytics**: AI-powered content recommendations
- [ ] **🚀 Auto-scaling**: Intelligent resource management

### 💡 Community Requested Features

Vote for features on our [GitHub Discussions](https://github.com/kasimlohar/kurukshetra/discussions):

- **🎥 Live Video Processing**: Real-time video analysis
- **🗣️ Voice Commands**: Voice-controlled interface
- **📋 Template System**: Pre-built workflow templates
- **🔄 Workflow Marketplace**: Community-shared workflows
- **📧 Email Integration**: Direct email document processing
- **🌐 Web Scraping**: Automated web content extraction

---

## 🧪 Testing & Quality

### 🔧 Development Workflow

```bash
# Install dependencies
npm install

# Development server with hot reload
npm run dev

# Type checking
npm run check

# Build for production
npm run build

# Build analysis (bundle size)
npm run build:analyze
```

### ✅ Accessibility Testing

The application includes comprehensive accessibility features:

- **Keyboard Navigation**: Full keyboard support with proper tab order
- **Screen Reader Support**: ARIA labels and semantic HTML structure  
- **Color Contrast**: WCAG AA compliant color schemes in both themes
- **Motion Preferences**: Respects `prefers-reduced-motion` setting
- **Focus Management**: Visible focus indicators and proper focus trapping
---

*© 2025 ConfluxAI. Licensed under MIT. Made with 💜 for the AI community.*

</div>
