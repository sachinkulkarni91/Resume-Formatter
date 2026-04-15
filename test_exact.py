import sys
resume_text = 'test'
def _truncate(r): return r

try:
    prompt = f\"\"\"You are a resume parsing engine. Extract ALL information from the resume below into structured JSON.

IMPORTANT: Extract EVERY SINGLE responsibility, project, date, technology, and line of experience from the resume. Do NOT skip, condense, or summarize ANY content. The output MUST contain 100% of the original bullet points unedited. If the resume is 7 pages, extract 7 pages worth of detail!

Return ONLY valid JSON with these fields:
{{
  "name": "",
  "title": "",
  "summary": {{
    "background": "full background paragraph here, if any",
    "bullets": ["exact bullet point 1", "exact bullet point 2"]
  }},
  "experience": [
    {{
      "role": "",
      "company": "",
      "client": "",
      "dates": "",
      "responsibilities": ["each responsibility as a separate item"],
      "technologies": ["each technology"],
      "projects": [
        {{
          "name": "",
          "client": "",
          "dates": "",
          "description": "",
          "technologies": ["tech1", "tech2"],
          "responsibilities": ["bullet 1", "bullet 2"]
        }}
      ]
    }}
  ],
  "skills": [
    {{
      "category": "category name",
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "certifications": [
    {{
      "name": "",
      "id": "",
      "date": "",
      "expires": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ]
}}

Resume:
{_truncate(resume_text)}\"\"\"
    print("SUCCESS!")
except Exception as e:
    print(f"FAILED: {e}")