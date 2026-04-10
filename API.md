# API Reference

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### Format Resume

**Endpoint:** `POST /api/format-resume`

**Description:** Convert a resume to match template formatting

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- target_resume (file, required): Resume to format (PDF/DOCX)
- template (file, required): Reference template (DOCX)
```

**Response:**
```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Body: Binary DOCX file
```

**Status Codes:**
- `200 OK` - Successfully formatted
- `400 Bad Request` - Invalid file format
- `413 Payload Too Large` - File too large
- `500 Internal Server Error` - Processing error

**Example:**
```bash
curl -X POST "http://localhost:8000/api/format-resume" \
  -F "target_resume=@resume.pdf" \
  -F "template=@template.docx" \
  -o formatted_resume.docx
```

**Python Example:**
```python
import requests

with open('resume.pdf', 'rb') as resume, open('template.docx', 'rb') as template:
    files = {
        'target_resume': resume,
        'template': template
    }
    response = requests.post(
        'http://localhost:8000/api/format-resume',
        files=files
    )
    
    if response.status_code == 200:
        with open('formatted_resume.docx', 'wb') as f:
            f.write(response.content)
    else:
        print(f"Error: {response.json()['detail']}")
```

---

### Parse Resume

**Endpoint:** `POST /api/parse-resume`

**Description:** Extract and structure resume content

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- resume (file, required): Resume file (PDF/DOCX)
```

**Response:**
```json
{
  "name": "John Doe",
  "title": "Senior Software Engineer",
  "summary": "Experienced software engineer with 10+ years...",
  "experience": [
    {
      "role": "Senior Engineer",
      "company": "Tech Corp",
      "client": "Enterprise Client",
      "dates": "2022-2024",
      "responsibilities": [
        "Led team of 5 engineers",
        "Designed scalable architecture"
      ],
      "technologies": ["Python", "AWS", "Kubernetes"]
    }
  ],
  "skills": {
    "Programming": ["Python", "JavaScript", "Go"],
    "Cloud": ["AWS", "GCP", "Azure"],
    "Management": ["Agile", "Team Leadership"]
  },
  "certifications": [
    {
      "name": "AWS Solutions Architect",
      "issuer": "Amazon",
      "date": "2022"
    }
  ],
  "education": [
    {
      "degree": "BS Computer Science",
      "school": "University of Tech",
      "year": "2014"
    }
  ],
  "projects": [
    {
      "title": "AI Resume Parser",
      "description": "Built ML pipeline for resume parsing",
      "technologies": ["Python", "TensorFlow"],
      "url": "https://github.com/user/project"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Successfully parsed
- `400 Bad Request` - Invalid file format
- `500 Internal Server Error` - Parsing error

**Example:**
```bash
curl -X POST "http://localhost:8000/api/parse-resume" \
  -F "resume=@resume.pdf" | jq .
```

**Python Example:**
```python
import requests
import json

with open('resume.pdf', 'rb') as f:
    files = {'resume': f}
    response = requests.post(
        'http://localhost:8000/api/parse-resume',
        files=files
    )
    
    parsed_data = response.json()
    print(json.dumps(parsed_data, indent=2))
```

---

### Extract Template

**Endpoint:** `POST /api/extract-template`

**Description:** Extract structure and styling from template

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- template (file, required): Template DOCX file
```

**Response:**
```json
{
  "styles": {
    "Heading 1": {
      "font_name": "Calibri",
      "font_size": 16,
      "bold": true,
      "italic": false,
      "underline": false,
      "color": null
    },
    "Normal": {
      "font_name": "Calibri",
      "font_size": 11,
      "bold": false,
      "italic": false,
      "underline": false,
      "color": null
    }
  },
  "sections": [
    {
      "text": "PROFESSIONAL EXPERIENCE",
      "style": "Heading 2",
      "level": "Heading 2",
      "alignment": "WD_ALIGN_PARAGRAPH.LEFT",
      "font": {
        "name": "Calibri",
        "size": 12,
        "bold": true,
        "italic": false
      }
    }
  ],
  "numbering": {},
  "tables": [
    {
      "rows": 5,
      "columns": 2,
      "width": 9144000
    }
  ],
  "margins": {
    "top": 914400,
    "bottom": 914400,
    "left": 914400,
    "right": 914400
  },
  "logo": {
    "exists": true,
    "relation_id": "rId4"
  }
}
```

**Status Codes:**
- `200 OK` - Successfully extracted
- `400 Bad Request` - Invalid file format
- `500 Internal Server Error` - Extraction error

**Example:**
```bash
curl -X POST "http://localhost:8000/api/extract-template" \
  -F "template=@template.docx" | jq .
```

---

### Suggest Improvements

**Endpoint:** `POST /api/suggest-improvements`

**Description:** Get ATS optimization and formatting suggestions

**Request:**
```
Content-Type: multipart/form-data

Parameters:
- resume (file, required): Resume file (PDF/DOCX)
```

**Response:**
```json
{
  "ats_score": 85,
  "strengths": [
    "Clean formatting",
    "Good keyword coverage",
    "Proper section structure"
  ],
  "weaknesses": [
    "Missing technical keywords",
    "Could improve summary section",
    "Some formatting inconsistencies"
  ],
  "keywords_to_add": [
    "Machine Learning",
    "DevOps",
    "Microservices",
    "CI/CD"
  ],
  "formatting_tips": [
    "Use consistent date format (MM/YYYY)",
    "Standardize bullet points",
    "Remove unnecessary special characters",
    "Ensure consistent spacing"
  ],
  "ats_friendly": true,
  "improvements_needed": 3
}
```

**Status Codes:**
- `200 OK` - Suggestions generated
- `400 Bad Request` - Invalid file format
- `500 Internal Server Error` - Analysis error

**Example:**
```bash
curl -X POST "http://localhost:8000/api/suggest-improvements" \
  -F "resume=@resume.pdf" | jq .
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid target resume format: txt"
}
```

### 413 Payload Too Large
```json
{
  "detail": "File too large"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error parsing PDF: [error description]"
}
```

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 413 | Payload Too Large |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

## Rate Limiting

- No explicit rate limiting in current version
- Recommended for production: 100 requests/hour per IP
- Implement exponential backoff for retries

---

## File Size Limits

| File Type | Max Size |
|-----------|----------|
| PDF | 50MB |
| DOCX | 50MB |
| DOC | 50MB |

---

## Supported File Formats

### Input Files
- `.pdf` - Portable Document Format
- `.docx` - Microsoft Word 2007+
- `.doc` - Microsoft Word 97-2003

### Output Files
- `.docx` - Microsoft Word 2007+ (OOXML)

---

## Authentication

Currently no authentication. For production, implement:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/format-resume")
async def format_resume(
    credentials: HTTPAuthCredentials = Depends(security),
    ...
):
    # Verify token
    pass
```

---

## Request Timeouts

- Default timeout: 300 seconds (5 minutes)
- Configurable via `TIMEOUT_SECONDS`
- Gemini API may take 10-30 seconds

---

## CORS Configuration

**Allowed Origins (configurable):**
```
http://localhost:3000
http://localhost:5173
https://yourdomain.com
```

**Allowed Methods:**
```
GET, POST, OPTIONS
```

**Allowed Headers:**
```
Content-Type, Authorization
```

---

## Testing with Postman

### Import Collection

1. Create new collection
2. Add requests for each endpoint
3. Add environment variables:
   - `base_url` = http://localhost:8000
   - `upload_dir` = path to test files

### Example Request

```
POST {{base_url}}/api/format-resume
Content-Type: multipart/form-data

target_resume: (file) resume.pdf
template: (file) template.docx
```

---

## WebSocket Support (Future)

Planned for real-time progress updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/format-resume');

ws.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(`Progress: ${progress.percentage}%`);
};
```

---

## Webhooks (Future)

Planned for async processing:

```bash
POST /api/format-resume-async
Content-Type: application/json

{
  "target_resume_url": "https://...",
  "template_url": "https://...",
  "webhook_url": "https://yourserver.com/callback"
}
```

Response:
```json
{
  "job_id": "uuid-here",
  "status": "processing",
  "webhook_url": "https://yourserver.com/callback"
}
```

---

## SDK Examples

### JavaScript/TypeScript

```typescript
import { ResumeFormatter } from '@resume-formatter/sdk';

const client = new ResumeFormatter({
  apiUrl: 'http://localhost:8000'
});

const formatted = await client.formatResume(
  targetResume,
  template
);

await formatted.save('formatted.docx');
```

### Python

```python
from resume_formatter import ResumeFormatter

client = ResumeFormatter(api_url='http://localhost:8000')

formatted_bytes = client.format_resume(
    target_resume_path='resume.pdf',
    template_path='template.docx'
)

with open('formatted.docx', 'wb') as f:
    f.write(formatted_bytes)
```

---

## Changelog

### v1.0.0 (Current)
- Resume parsing with Gemini AI
- Template extraction
- DOCX generation with formatting
- ATS suggestions
- Web UI

### v1.1.0 (Planned)
- WebSocket real-time updates
- Async processing
- Batch resume processing
- User authentication
- Premium features

