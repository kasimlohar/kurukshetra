# 🤖 ConfluxAI - AI-Powered Multi-Media Knowledge Base

<div align="center">

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/kasimlohar/kurukshetra)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-43853D?logo=node.js&logoColor=white)](https://nodejs.org/)

</div>

## 📖 Overview

ConfluxAI is a sophisticated AI-powered multi-media knowledge base that processes documents, images, videos, and audio files using intelligent n8n workflows. Chat with your uploaded content using natural language and get instant, contextual responses powered by Google Gemini AI.

### ✨ Key Features

- 🧠 **AI-Powered Chat Interface** - Intelligent conversations about your uploaded content
- 📄 **PDF Processing** - Extract and analyze document content
- 🖼️ **Image Analysis** - Visual content recognition and description
- 🎬 **Video Processing** - Transcription and content analysis
- 🎵 **Audio Transcription** - Convert speech to searchable text
- 🔄 **n8n Workflow Integration** - Automated processing pipelines
- 🎨 **Modern React UI** - Responsive design with dark/light themes
- 🔐 **Secure Authentication** - Protected routes and user sessions
- 📊 **Document Management** - Track and organize your uploads

## 🖼️ Screenshots

### Main Interface
![Main Interface](docs/screenshots/main-interface.png)
*Clean, modern dashboard with file upload capabilities*

### Chat Interface
![Chat Interface](docs/screenshots/chat-interface.png)
*Intelligent AI chat powered by Google Gemini*

### File Upload System
![File Upload](docs/screenshots/file-upload.png)
*Drag & drop file upload with progress tracking*

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ 
- **npm** or **yarn**
- **n8n** instance (optional for custom workflows)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kasimlohar/kurukshetra.git
   cd kurukshetra/ConfluxAI
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment setup**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Build the frontend**
   ```bash
   npm run build
   ```

5. **Start development server**
   ```bash
   npm run dev:vercel
   ```

### 🖥️ Quick Start Scripts

For **Windows**:
```bash
.\start-local.bat
```

For **Linux/macOS**:
```bash
chmod +x start-local.sh
./start-local.sh
```

Your application will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file with the following variables:

```env
# Application Environment
NODE_ENV=development

# n8n Webhook URLs (Production)
N8N_PDF_WEBHOOK_URL=https://your-n8n-instance.com/webhook/pdf-ingest
N8N_IMAGE_WEBHOOK_URL=https://your-n8n-instance.com/webhook/image-ingest
N8N_VIDEO_WEBHOOK_URL=https://your-n8n-instance.com/webhook/video-process
N8N_AUDIO_WEBHOOK_URL=https://your-n8n-instance.com/webhook/audio-process
N8N_CHAT_WEBHOOK_URL=https://your-n8n-instance.com/webhook/chat-agent

# n8n Webhook URLs (Test)
N8N_PDF_WEBHOOK_TEST_URL=https://your-n8n-instance.com/webhook-test/pdf-ingest
N8N_IMAGE_WEBHOOK_TEST_URL=https://your-n8n-instance.com/webhook-test/image-ingest
N8N_VIDEO_WEBHOOK_TEST_URL=https://your-n8n-instance.com/webhook-test/video-process
N8N_AUDIO_WEBHOOK_TEST_URL=https://your-n8n-instance.com/webhook-test/audio-process
N8N_CHAT_WEBHOOK_TEST_URL=https://your-n8n-instance.com/webhook-test/chat-agent
```

## 🏗️ Architecture

### Frontend
- **React 18.3** with TypeScript
- **Vite 5.4** for fast development and building
- **Tailwind CSS 3.4** for styling
- **shadcn/ui** components for consistent UI
- **React Query** for state management

### Backend
- **Express.js 4.21** server
- **Vercel** serverless functions for production
- **Multer 2.0** for file uploads
- **Session-based authentication**

### AI & Automation
- **n8n workflows** for content processing
- **Google Gemini API** for AI responses
- **Pinecone vector database** for semantic search
- **LangChain agents** for intelligent processing

## 📁 Project Structure

```
ConfluxAI/
├── 📱 client/                    # React frontend
│   ├── src/
│   │   ├── components/          # UI components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom React hooks
│   │   └── lib/                # Utility functions
│   └── dist/                   # Build output
├── 🚀 api/                      # Vercel serverless functions
│   ├── webhook/                # n8n webhook handlers
│   ├── upload-*.ts             # File upload endpoints
│   └── dev-server.ts           # Development server
├── 🤖 n8n_workflows/           # Automation workflows
│   ├── AI agent.json           # Main AI agent workflow
│   ├── pdf_saving_func.json    # PDF processing
│   ├── image processing.json   # Image analysis
│   ├── video processing.json   # Video processing
│   └── audio processing.json   # Audio transcription
├── 📚 docs/                    # Documentation
│   └── screenshots/            # UI screenshots
└── 🗄️ server/                  # Express server (legacy)
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/webhook/n8n` | POST | Chat and AI processing |
| `/api/upload-pdf` | POST | PDF document upload |
| `/api/upload-image` | POST | Image upload and analysis |
| `/api/upload-video` | POST | Video upload and processing |
| `/api/upload-audio` | POST | Audio upload and transcription |

## 📄 Supported File Types

| Type | Formats | Max Size |
|------|---------|----------|
| **Documents** | PDF | 10MB |
| **Images** | JPG, PNG, GIF, WebP | 10MB |
| **Videos** | MP4, AVI, MOV, WebM | 100MB |
| **Audio** | MP3, WAV, OGG, M4A | 50MB |

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect your repository** to Vercel
2. **Configure build settings**:
   - Framework: Other
   - Build Command: `npm run build`
   - Output Directory: `client/dist`
3. **Add environment variables** in Vercel dashboard
4. **Deploy** 🎉

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Docker (Coming Soon)

```bash
# Build and run with Docker
docker build -t conflux-ai .
docker run -p 5000:5000 conflux-ai
```

## 🧪 Development

### Available Scripts

```bash
npm run dev          # Start Express development server
npm run dev:vercel   # Start Vercel-compatible dev server
npm run build        # Build for production
npm run check        # TypeScript type checking
npm run db:push      # Push database schema changes
```

### Development Workflow

1. **Start development server**
   ```bash
   npm run dev:vercel
   ```

2. **Make changes** to the code
3. **Test locally** at `http://localhost:5000`
4. **Build and deploy** when ready

## 🧩 n8n Workflows

The project includes pre-built n8n workflows for:

- **AI Agent** - Main chat and reasoning agent
- **PDF Processing** - Document extraction and indexing
- **Image Analysis** - Visual content recognition
- **Video Processing** - Transcription and analysis
- **Audio Processing** - Speech-to-text conversion

Import these workflows into your n8n instance to get started quickly.

## 🔐 Security

- ✅ **Input validation** and sanitization
- ✅ **Secure file upload** handling
- ✅ **Session-based authentication**
- ✅ **Environment variable protection**
- ✅ **HTTPS enforcement** in production
- ✅ **Rate limiting** on API endpoints

See [SECURITY.md](SECURITY.md) for security policy and reporting vulnerabilities.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- 📋 Code of conduct
- 🛠️ Development setup
- 📝 Coding standards
- 🔄 Pull request process

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and new features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Kasim Lohar** - [@kasimlohar](https://github.com/kasimlohar)

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent responses
- **n8n** for workflow automation
- **Vercel** for hosting and deployment
- **shadcn/ui** for beautiful UI components
- **React** and **TypeScript** communities

## 📞 Support

- 📧 **Email**: kasimlohar@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/kasimlohar/kurukshetra/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/kasimlohar/kurukshetra/discussions)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[Live Demo](https://conflux-ai.vercel.app) | [Documentation](docs/) | [Changelog](CHANGELOG.md)

</div>
