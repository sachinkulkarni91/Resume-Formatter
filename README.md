# Resume Formatter - Full Stack Application

A production-ready full-stack application that converts any resume into a reference template format (KPMG-style Word document) with pixel-perfect accuracy using **Google Gemini (via Gemini API)**.

## 🎯 Features

✅ **Resume Parsing** - Extract and structure resume content from PDF/DOCX
✅ **Gemini Integration** - AI-powered resume structuring and mapping  
✅ **Template Matching** - Extract formatting from reference documents
✅ **Document Generation** - Generate perfectly formatted DOCX files
✅ **ATS Optimization** - Get suggestions for improving resume quality
✅ **Web UI** - Beautiful React-based frontend for easy interaction
✅ **REST API** - FastAPI backend with comprehensive endpoints

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                            │
│              (Upload, Preview, Download UI)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (main.py)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  · /api/format-resume  - Main formatting endpoint        │   │
│  │  · /api/parse-resume   - Parse resume to JSON            │   │
│  │  · /api/extract-template - Extract template structure    │   │
│  │  · /api/suggest-improvements - ATS suggestions           │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬──────────────┐
        ▼                ▼                ▼              ▼
    ┌────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐
    │ Parser │    │  Gemini  │    │ Template  │    │ DocXGen  │
    │(PDF,   │    │ Service  │    │ Engine    │    │          │
    │DOCX)   │    │(AI)      │    │(Styles)   │    │(Output)  │
    └────────┘    └──────────┘    └───────────┘    └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn
- Google Gemini API Key

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env if needed (default points to localhost:8000)
```

### 3. Run Applications

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
# API will run on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# App will run on http://localhost:5173
```

## 🔑 Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key" → "Create API Key in new project"
3. Copy the key
4. Add it to your `.env` file: `GEMINI_API_KEY=your_key_here`

## 📖 API Documentation

### Format Resume (Main Endpoint)

**POST** `/api/format-resume`

Convert a resume to match template formatting.

**Request:**
```
Content-Type: multipart/form-data

- target_resume: File (PDF/DOCX) - Resume to format
- template: File (DOCX) - Reference template
```

**Response:**
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

Downloads formatted_resume.docx
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/api/format-resume" \
  -F "target_resume=@resume.pdf" \
  -F "template=@template.docx"
```

### Parse Resume

**POST** `/api/parse-resume`

Extract and structure resume content.

**Request:**
```
Content-Type: multipart/form-data

- resume: File (PDF/DOCX)
```

**Response:**
```json
{
  "name": "John Doe",
  "title": "Software Engineer",
  "summary": "...",
  "experience": [
    {
      "role": "Senior Engineer",
      "company": "Tech Corp",
      "dates": "2020-2024",
      "responsibilities": ["..."],
      "technologies": ["..."]
    }
  ],
  "skills": {...},
  "certifications": [...],
  "education": [...],
  "projects": [...]
}
```

### Extract Template

**POST** `/api/extract-template`

Extract structure from reference document.

**Request:**
```
Content-Type: multipart/form-data

- template: File (DOCX)
```

**Response:**
```json
{
  "styles": {...},
  "sections": [...],
  "numbering": {...},
  "tables": [...],
  "margins": {...},
  "logo": {...}
}
```

### Suggest Improvements

**POST** `/api/suggest-improvements`

Get ATS optimization suggestions.

**Request:**
```
Content-Type: multipart/form-data

- resume: File (PDF/DOCX)
```

**Response:**
```json
{
  "ats_score": 85,
  "suggestions": ["..."],
  "keywords_to_add": ["..."],
  "formatting_tips": ["..."]
}
```

## 🔧 Backend Structure

```
backend/
├── main.py               # FastAPI application & endpoints
├── config.py             # Configuration settings
├── gemini_service.py     # Gemini API integration
├── parser.py             # Resume & template parsing
├── template_engine.py    # Template styling & formatting
├── doc_generator.py      # DOCX document generation
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── uploads/              # Temporary upload storage
```

### Key Files Explained

**main.py**
- FastAPI application setup
- All REST API endpoints
- File upload handling
- CORS configuration

**gemini_service.py**
- Gemini API calls for:
  - Resume parsing (structured extraction)
  - Template mapping (content alignment)
  - ATS suggestions

**parser.py**
- PDF extraction via pdfplumber
- DOCX extraction via python-docx
- Template structure analysis

**template_engine.py**
- Extract styles from reference document
- Copy formatting to new document
- Apply heading styles and numbering

**doc_generator.py**
- Generate DOCX from structured data
- Apply formatting and styling
- Support for sections, tables, lists

## 💻 Frontend Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main app component & logic
│   ├── App.css          # Application styling
│   ├── FileUpload.jsx   # File upload component
│   ├── FileUpload.css   # Upload component styling
│   ├── api.js           # API client functions
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies
└── .env.example         # Environment template
```

## 🎨 Features Explained

### 1. Resume Formatting
- Upload any resume (PDF/DOCX)
- Select a reference template
- System extracts content and reformats to match template style
- Download perfectly formatted DOCX

### 2. Resume Parsing
- Parse resume to structured JSON
- Extract: name, title, experience, skills, education, certifications, projects
- AI-powered using Gemini for intelligent extraction

### 3. Template Extraction
- Upload reference template
- Extract all styling information
- Get complete structure for reference

### 4. ATS Optimization
- Upload resume
- Get optimization suggestions
- Improve keyword coverage
- Check formatting for ATS systems

## 🌐 Environment Variables

**Backend (.env)**
```
GEMINI_API_KEY=your_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:8000
```

## 📦 Production Deployment

### Backend (Python 3.11+)

```bash
# Install with production dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Node 18+)

```bash
# Build for production
npm run build

# Serve with production server
npm install -g serve
serve -s dist -l 3000
```

### Docker Deployment

**Backend Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## ⚡ Performance Tips

1. **Optimize Resume Uploads**
   - Keep PDFs under 10MB
   - Use DOCX format for faster parsing
   - Avoid scanned images

2. **Template Best Practices**
   - Use clean, simple templates
   - Avoid complex nested tables
   - Keep consistent formatting

3. **API Rate Limiting**
   - Gemini has rate limits
   - Implement request throttling in production
   - Cache parsed results when possible

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file in backend directory and add your API key

### Issue: CORS errors
**Solution:** Check CORS_ORIGINS in `.env` matches frontend URL

### Issue: PDF parsing fails
**Solution:** Ensure PDF is not scanned image, convert to text-based PDF

### Issue: Template formatting not applied
**Solution:** Ensure template document has consistent styles throughout

## 🚀 Advanced Usage

### Bulk Resume Processing

```python
from gemini_service import GeminiService
from parser import ResumeParser
from doc_generator import DocxGenerator

gemini = GeminiService()

for resume_file in resume_files:
    text = ResumeParser.parse(resume_file)
    parsed = gemini.parse_resume(text)
    doc = DocxGenerator(template_path)
    doc.generate_from_structured_data(parsed)
    doc.save(f"formatted_{resume_file.stem}.docx")
```

### Custom Resume Mapping

Modify `gemini_service.py` to customize how content is mapped:

```python
def map_to_template(self, parsed_resume, template_structure):
    # Add custom mapping logic
    # Customize before calling Gemini
    ...
```

## 📝 License

This project is licensed under MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Made with ❤️ using FastAPI, React, and Google Gemini**
