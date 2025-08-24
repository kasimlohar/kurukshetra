# 🔍 ConfluxAI - Multi-Modal AI Search Agent

[![Kurukshetra 2025](https://img.shields.io/badge/Kurukshetra-2025-orange)](https://linktr.ee/MozillaMitACSC)
[![AI/ML Theme](https://img.shields.io/badge/Theme-AI%2FML%20%26%20Agentic%20AI-blue)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent AI research assistant that revolutionizes information discovery by seamlessly searching across text, images, tables, and documents simultaneously. Built for researchers, students, and professionals who need comprehensive, citation-grounded insights from diverse data sources.

> *"Bridging the gap between scattered information and unified knowledge discovery"*

---

## 🎯 Problem Statement (Kurukshetra 2025)

**Multi-Modal AI Search Agent**: Build an AI agent that can search across text, images, and documents simultaneously.

### Key Challenges Addressed:
- ✅ **Multi-modal embedding alignment** (text vs. image vs. structured table regions)
- ✅ **Semantic ranking** across different content types
- ✅ **Result summarization** with proper citations
- ✅ **Cross-modal search** capabilities

---

## 🚀 Core Features

### 🔄 Multi-Modal Ingestion
- **PDF Processing**: Extract text, tables, figures, and captions
- **Web Scraping**: Clean HTML content with structured data extraction
- **Image Analysis**: OCR and visual content understanding
- **Document Parsing**: Support for various file formats

### 🧠 Intelligent Search
- **Semantic Search**: Dense vector embeddings for contextual understanding
- **Hybrid Retrieval**: Combines dense + sparse (BM25) ranking
- **Cross-Modal Queries**: Find relevant content across all modalities
- **Smart Reranking**: Modality-aware scoring with proximity analysis

### 📊 Grounded Summarization
- **Citation-Enforced**: Every claim backed by source references
- **Multi-Modal Results**: Text passages, table data, and figure insights
- **JSON Output**: Structured responses with metadata
- **Visual References**: Direct links to figures and tables

---

## 🏗️ Architecture Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Ingestion  │ -> │ Normalizer  │ -> │   Chunker   │
│   Pipeline  │    │   Module    │    │   Engine    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
   PDF Parser          Web Scraper        Image OCR
   Table Extract       HTML Cleaner       Caption Gen
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
              ┌─────────────────────────┐
              │   Embedding Pipeline    │
              │ Text + Image Encoders   │
              │  Alignment Projection   │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   Vector Store +        │
              │    Metadata DB          │
              │  (pgvector/Qdrant)      │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   Hybrid Retrieval      │
              │ Dense + Sparse + Rerank │
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   Answer Generator      │
              │ Citation-Constrained LLM│
              └─────────────────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  Multi-Modal UI         │
              │ Interactive Results     │
              └─────────────────────────┘
```

---

## 📋 Data Model

| Field | Description | Type |
|-------|-------------|------|
| `id` | Unique chunk identifier | UUID |
| `source_id` | Original file/URL reference | String |
| `modality` | Content type: text/table/figure/image | Enum |
| `content_text` | Cleaned textual content or caption | Text |
| `content_blob` | Serialized image/table data | BLOB |
| `vector` | Dense embedding (1536d) | Vector |
| `tokens` | Token count for cost estimation | Integer |
| `page_num` | PDF page number (if applicable) | Integer |
| `bbox` | Normalized coordinates for highlighting | JSON |
| `metadata` | Headers, alt text, table schema | JSON |

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **PDF Processing** | pdfplumber, PyMuPDF | Text & layout extraction |
| **Table Extraction** | Camelot, pdfplumber | Structured data parsing |
| **Web Scraping** | Playwright, trafilatura | Clean content extraction |
| **OCR Engine** | Tesseract, PaddleOCR | Image text recognition |
| **Text Embeddings** | OpenAI text-embedding-3-large | Semantic vectors |
| **Image Embeddings** | CLIP, SigLIP | Visual understanding |
| **Vector Database** | PostgreSQL pgvector | Scalable similarity search |
| **Backend API** | FastAPI | High-performance API |
| **Reranking** | bge-reranker | Cross-encoder scoring |
| **LLM Integration** | OpenAI GPT-4 | Citation-grounded summaries |
| **Frontend** | React, TypeScript | Interactive UI |
| **Workflow** | n8n | Automation pipeline |

---

## 🎯 Retrieval Strategy

### 1. Query Processing
- Embed user query using text encoder
- Extract key entities and intent

### 2. Candidate Generation
- **Dense Search**: kNN vector similarity
- **Sparse Search**: BM25 keyword matching
- **Hybrid Fusion**: Reciprocal rank fusion

### 3. Modality-Aware Reranking
```
score = α × dense_sim + β × sparse_sim + γ × modality_boost + δ × structural_proximity
```

### 4. Diversification
- Avoid over-clustering on single pages
- Ensure modality balance in results

### 5. Citation Preparation
- Pass top-N chunks to summarizer with strict citation enforcement

---

## 📊 Output Schema

```json
{
  "answer": "The proposed model outperforms baselines through architectural improvements...",
  "citations": [
    {
      "chunk_id": "T07",
      "page": 6,
      "modality": "table",
      "source": "research_paper.pdf"
    },
    {
      "chunk_id": "F12",
      "page": 4,
      "modality": "figure",
      "source": "research_paper.pdf"
    }
  ],
  "figures": [
    {
      "chunk_id": "F12",
      "caption": "Architecture comparison showing 15% improvement",
      "page": 4
    }
  ],
  "confidence": 0.89,
  "query_time_ms": 847
}
```

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.9+
pip install -r requirements.txt

# Node.js 18+ (for frontend)
npm install

# PostgreSQL with pgvector extension
# Or Docker setup (recommended)
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Configure your API keys
OPENAI_API_KEY=your_openai_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

### Running the Application

#### Backend
```bash
# Start the API server
python -m uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
# Start the React development server
npm run dev
```

#### n8n Workflows (Optional)
```bash
# Import automation workflows
npm run import-workflows
```

---

## 💡 Demo Scenarios

### Research Assistant Demo
1. **Upload**: Research paper with tables and diagrams
2. **Query**: "Compare model accuracy and architectural components"
3. **Results**: 
   - Mixed modality results (text + figures + tables)
   - Grounded answer with inline citations
   - Interactive citation highlighting
4. **Export**: Formatted report with sources

### Example Queries
- *"What are the main performance improvements over baseline methods?"*
- *"Show me all tables related to accuracy metrics"*
- *"Find architectural diagrams that explain the model design"*
- *"Compare results across different datasets"*

---

## 📈 Evaluation Metrics

| Metric | Method | Target |
|--------|--------|--------|
| **Retrieval Precision@5** | Labeled relevance sets | >0.85 |
| **Rerank Gain** | nDCG improvement | >15% |
| **Answer Faithfulness** | Citation coverage % | >90% |
| **Query Latency** | End-to-end response | <2s |
| **Multi-Modal Coverage** | Result diversity | Balanced |

---

## 🎯 Hackathon Roadmap

### Day 1 Morning (24th Aug 9:00-13:00)
- [x] PDF + web ingestion pipeline
- [x] Basic text + caption embedding
- [x] Vector database setup

### Day 1 Evening (24th Aug 14:00-21:00)
- [x] Hybrid retrieval implementation
- [x] Simple query interface
- [x] Basic result display

### Day 2 Morning (25th Aug 6:00-10:00)
- [x] Reranking algorithm
- [x] Citation-based summarization
- [x] Multi-modal result panel

### Day 2 Final (25th Aug 10:00-12:30)
- [x] Demo preparation
- [x] Evaluation examples
- [x] Final polish & testing

---

## 🔮 Future Enhancements

- **Query Refinement**: Auto-generated facets and suggestions
- **Visual Similarity**: Upload image to find similar content
- **Temporal Awareness**: Time-based result weighting
- **Confidence Scoring**: Answer reliability metrics
- **Multi-Language Support**: Cross-language search capabilities

---

## ⚠️ Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Embedding Mismatch** | Poor cross-modal results | CLIP projection alignment |
| **Noisy OCR** | Inaccurate text extraction | Confidence filtering + fallbacks |
| **Hallucinated Summaries** | Unreliable answers | Strict citation enforcement |
| **High Latency** | Poor user experience | Embedding caching + batch queries |
| **Scale Limitations** | Performance degradation | Efficient indexing + query optimization |

---

## 👥 Team Contributions

| Role | Contributor | Responsibilities |
|------|-------------|------------------|
| **Data Engineering** | [Name] | Ingestion pipeline, preprocessing |
| **ML/AI Research** | [Name] | Embedding models, retrieval algorithms |
| **Backend Development** | [Name] | API design, database optimization |
| **Frontend Development** | [Name] | UI/UX, user interface |
| **DevOps & Demo** | [Name] | Deployment, demo preparation |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgments

- **Kurukshetra 2025** - Mozilla MIT ACSC for the inspiring hackathon
- **Open Source Community** - For the amazing tools and libraries
- **Research Community** - For advancing multi-modal AI techniques

---

## 📞 Contact & Support

- **Demo Video**: [YouTube Link](#)
- **Live Demo**: [Deployed App](#)
- **GitHub Issues**: [Report Issues](../../issues)
- **Team Email**: [confluxai.team@email.com](#)

---

### 🎯 Hackathon Judges

**ConfluxAI** represents the future of intelligent information discovery - where every search transcends modality boundaries to deliver comprehensive, trustworthy insights. Our solution directly addresses the critical need for unified semantic search across diverse content types, making research and knowledge discovery more efficient and reliable than ever before.

*Ready to revolutionize how we search and discover information? Let's make it happen at Kurukshetra 2025!* 🚀

---

**Built with ❤️ for Kurukshetra 2025 Hackathon**