# Setup Instructions

## Initial Setup Guide

### 1. Clone/Extract Project

Extract the Resume Formatter project to your desired location.

### 2. Obtain Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" → "Create API Key in new project"
4. Copy the generated API key

### 3. Backend Configuration

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_key_here_without_quotes
```

### 4. Frontend Configuration

```bash
cd ../frontend

# Install Node dependencies
npm install

# Create .env file (optional, defaults work fine)
cp .env.example .env
```

### 5. Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.8  ready in 123 ms

➜  Local:   http://localhost:5173/
```

### 6. Access the Application

Open your browser and go to: **http://localhost:5173**

## File Structure

```
Resume-Formatter/
├── backend/
│   ├── main.py                # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── gemini_service.py      # Gemini API integration
│   ├── parser.py              # File parsing logic
│   ├── template_engine.py     # Template handling
│   ├── doc_generator.py       # Document generation
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   ├── .env                   # (Create this with your API key)
│   ├── uploads/               # Temporary file storage
│   └── outputs/               # Generated documents
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main application
│   │   ├── FileUpload.jsx     # Upload component
│   │   ├── api.js             # API calls
│   │   └── styles/            # CSS files
│   ├── index.html             # HTML template
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite config
│   └── .env.example           # Environment template
└── README.md                  # Full documentation
```

## Usage Guide

### Basic Workflow

1. **Upload Target Resume**
   - Click "Select Files" or drag & drop
   - Choose your resume (PDF or DOCX)

2. **Upload Reference Template**
   - Click "Select Files" or drag & drop
   - Choose your reference template (must be DOCX)

3. **Format Resume**
   - Click "Format Resume" button
   - Wait for processing (usually 10-30 seconds)
   - Download the formatted resume

### Additional Features

**Parse Resume**
- Extract structured data from any resume
- See all parsed sections in JSON format
- Useful for validation

**Suggestions Tab**
- Get ATS optimization tips
- See keyword recommendations
- Improve formatting suggestions

## Troubleshooting

### Backend Won't Start

**Error: "No module named 'fastapi'"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt
```

**Error: "GEMINI_API_KEY not found"**
1. Check that `.env` file exists in backend directory
2. Verify GEMINI_API_KEY is set correctly
3. Make sure there are no extra spaces in the key

### Frontend Won't Start

**Error: "npm: command not found"**
- Install Node.js from nodejs.org
- Restart your terminal

**Port 5173 already in use:**
```bash
# Try alternative port
npm run dev -- --port 3000
```

### API Connection Issues

**Error: "Failed to connect to backend"**
1. Ensure backend is running on port 8000
2. Check CORS_ORIGINS in backend/.env
3. Frontend should be at http://localhost:5173 or equivalent

### Resume Formatting Issues

**No output generated:**
- Check backend logs for detailed errors
- Ensure template is a valid DOCX file
- Try with smaller PDF files first

**Formatting doesn't match template:**
- Ensure template has consistent styles
- Check if template uses complex nested tables
- Try simplifying the template

## Performance Optimization

### For Production

**Backend:**
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Frontend:**
```bash
# Build for production
npm run build

# Results in optimized dist/ folder
# Serve with any static server or upload to hosting
```

### Recommended Hosting

**Backend:**
- Heroku
- Railway
- AWS EC2
- Google Cloud Run
- DigitalOcean

**Frontend:**
- Vercel (recommended for Vite)
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Cloudflare Pages

## API Testing

### With cURL

```bash
# Format resume
curl -X POST "http://localhost:8000/api/format-resume" \
  -F "target_resume=@resume.pdf" \
  -F "template=@template.docx" \
  -o formatted_resume.docx

# Parse resume
curl -X POST "http://localhost:8000/api/parse-resume" \
  -F "resume=@resume.pdf"

# Extract template
curl -X POST "http://localhost:8000/api/extract-template" \
  -F "template=@template.docx"

# Get suggestions
curl -X POST "http://localhost:8000/api/suggest-improvements" \
  -F "resume=@resume.pdf"
```

### With Python

```python
import requests

# Format resume
with open('resume.pdf', 'rb') as resume, open('template.docx', 'rb') as template:
    files = {
        'target_resume': resume,
        'template': template
    }
    response = requests.post('http://localhost:8000/api/format-resume', files=files)
    with open('formatted_resume.docx', 'wb') as f:
        f.write(response.content)

# Parse resume
with open('resume.pdf', 'rb') as resume:
    files = {'resume': resume}
    response = requests.post('http://localhost:8000/api/parse-resume', files=files)
    print(response.json())
```

## Next Steps

1. **Explore the Code** - Understand how parsing, AI mapping, and document generation work
2. **Customize** - Modify prompts in `gemini_service.py` for your needs
3. **Extend** - Add new features or integrations
4. **Deploy** - Set up production environment
5. **Feedback** - Report issues and suggest improvements

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python main.py` | Start backend API |
| `npm run dev` | Start frontend dev server |
| `npm run build` | Build frontend for production |
| `pip install -r requirements.txt` | Install backend dependencies |
| `npm install` | Install frontend dependencies |

## Support

For issues, visit the README.md or check the backend logs with:
```bash
# Windows
type backend/uploads/*.log

# Linux/Mac
tail -f backend/uploads/*.log
```

Enjoy! 🚀
