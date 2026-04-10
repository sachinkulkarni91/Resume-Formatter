# Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Get Gemini API Key (1 minute)

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key ✓

### Step 2: Clone & Configure (2 minutes)

```bash
# Navigate to project
cd Resume-Formatter

# Backend setup
cd backend
cp .env.example .env
# Edit .env and paste your Gemini API key

# Frontend setup
cd ../frontend
cp .env.example .env
```

### Step 3: Install Dependencies (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
```

### Step 4: Run! (1 minute)

**Terminal 1:**
```bash
cd backend
python main.py
# ✓ API running at http://localhost:8000
```

**Terminal 2:**
```bash
cd frontend
npm run dev
# ✓ Frontend at http://localhost:5173
```

### Step 5: Try It!

1. Open http://localhost:5173
2. Upload any resume (PDF or DOCX)
3. Upload a reference template (DOCX)
4. Click "Format Resume"
5. Download your formatted resume! 🎉

---

## 📚 Common Tasks

### Upload & Format Resume

1. **Step 1:** Click "Select Files" or drag resume
2. **Step 2:** Click "Select Files" for template or drag
3. **Step 3:** Click "Format Resume"
4. **Step 4:** Wait 10-30 seconds
5. **Step 5:** Download formatted resume

### Parse Resume to JSON

1. Go to "Parse Resume" tab
2. Upload resume
3. Click "Parse Resume"
4. View structured data

### Get Suggestions

1. Go to "Suggestions" tab
2. Upload resume
3. Click "Get Suggestions"
4. Review ATS tips

---

## 🔑 API Testing

### Quick API Test (cURL)

```bash
# Format resume
curl -X POST http://localhost:8000/api/format-resume \
  -F "target_resume=@resume.pdf" \
  -F "template=@template.docx" \
  -o formatted.docx

# Parse resume
curl -X POST http://localhost:8000/api/parse-resume \
  -F "resume=@resume.pdf" | jq .

# Extract template
curl -X POST http://localhost:8000/api/extract-template \
  -F "template=@template.docx" | jq .

# Get suggestions
curl -X POST http://localhost:8000/api/suggest-improvements \
  -F "resume=@resume.pdf" | jq .
```

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Change in backend/main.py line 180 |
| Port 5173 in use | Run `npm run dev -- --port 3000` |
| GEMINI_API_KEY error | Check backend/.env has correct key |
| Module not found | Run `pip install -r requirements.txt` |
| npm: command not found | Install Node.js from nodejs.org |
| CORS error | Verify backend CORS_ORIGINS in .env |
| Upload fails | Check file size < 50MB |
| No output | Check backend logs for Gemini errors |

---

## 📁 Project Structure

```
Resume-Formatter/
├── backend/           ← Python API
│   ├── main.py       (Start here!)
│   └── .env          (Your API key)
├── frontend/          ← React UI
│   ├── src/App.jsx   (Main app)
│   └── package.json
└── README.md         (Full docs)
```

---

## 🚀 Next Steps

1. **Upload test resume** - Try formatting
2. **Play with templates** - Test different styles
3. **Review API docs** - In API.md
4. **Deploy** - See DEPLOYMENT.md
5. **Customize** - Modify prompts in backend/gemini_service.py

---

## 💡 Pro Tips

### Tip 1: Test with Sample Files
```bash
# Keep test documents ready
# PDF: any resume file
# DOCX: any resume or template
```

### Tip 2: Check Logs
```bash
# Backend logs show everything
# Frontend console (F12 in browser)
```

### Tip 3: Use Postman
- Import API collection
- Test endpoints graphically
- Save requests

### Tip 4: Monitor Gemini Usage
- Check Google AI Studio dashboard
- Monitor API costs
- Note: Free tier has limits

---

## 📞 Getting Help

- **Error?** Check terminal logs first
- **Stuck?** Read README.md in detail
- **API issue?** See API.md
- **Deploy?** Check DEPLOYMENT.md
- **Contribute?** See CONTRIBUTING.md

---

## ✨ What's Included

✅ FastAPI backend with Gemini integration  
✅ React frontend with file upload UI  
✅ PDF & DOCX parsing  
✅ Template extraction  
✅ Document generation  
✅ ATS suggestions  
✅ Docker support  
✅ Full documentation  
✅ CI/CD workflows  
✅ Production-ready code  

---

## 🎯 Common Use Cases

### Use Case 1: Format Resume to KPMG Style
1. Upload your resume
2. Upload KPMG template
3. Download formatted resume
4. Done!

### Use Case 2: Batch Process Multiple Resumes
```python
# Use Python script in backend/
for resume in resumes:
    formatted = format_resume(resume, template)
    save(formatted)
```

### Use Case 3: Get Resume Insights
1. Upload resume
2. Use "Parse Resume" tab
3. View JSON structure
4. Use data for analysis

### Use Case 4: ATS Optimization
1. Upload resume
2. Go to "Suggestions" tab
3. Review improvement tips
4. Update resume accordingly

---

## 📊 Performance Tips

- **Upload time:** < 5 seconds
- **Processing time:** 10-30 seconds (includes Gemini)
- **Download:** Instant
- **Best time:** Off-peak hours (fewer API calls)
- **File size:** Keep under 10MB for fast processing

---

## 🔐 Security Notes

- API keys stored in .env (never commit)
- Files deleted after processing
- No data stored on server
- HTTPS recommended for production
- File size limits (50MB max)

---

## 📈 Success Indicators

✓ Backend running on port 8000  
✓ Frontend running on port 5173  
✓ GEMINI_API_KEY configured  
✓ No errors in console  
✓ Able to upload files  
✓ Network requests succeeding  
✓ Formatted document generated  

---

## 🎓 Learn More

Read the full documentation:
- **README.md** - Overview & features
- **SETUP.md** - Detailed setup
- **API.md** - API reference
- **DEPLOYMENT.md** - Production
- **CONTRIBUTING.md** - Development

---

## 🎉 You're Ready!

Enjoy using Resume Formatter! 

Questions? Check README.md or SETUP.md.

