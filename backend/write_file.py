content = '''import json
import re
from openai import OpenAI
from config import GROQ_API_KEY, GROQ_MODEL
from typing import Dict, Any
from json_repair import repair_json

class GeminiService:
    \"\"\"Service for interacting with Ollama via OpenAI client\"\"\"

    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama", # API key is required by the SDK but ignored by Ollama
        )
        self.model = "llama3.2:1b" # A much smaller model that fits in your available memory

    def _extract_and_parse_json(self, response_text: str) -> Dict[str, Any]:
        \"\"\"Validates, cleans, and attempts to automatically repair any malformed JSON strings.\"\"\"
        if response_text.startswith("`json"):
            response_text = response_text[7:]
        elif response_text.startswith("`"):
            response_text = response_text[3:]
            
        if response_text.endswith("`"):
            response_text = response_text[:-3]

        response_text = response_text.strip()
        
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            response_text = match.group(0)
            
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            try:
                repaired = repair_json(response_text, return_objects=True)
                return repaired if isinstance(repaired, dict) else {}
            except Exception as e:
                raise ValueError(f"CRITICAL: Failed to parse or repair LLM response. Original Error: {e}\\nResponse Preview: {response_text[:200]}...")

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        \"\"\"
        Parse resume text and convert to structured JSON using the LLM.
        \"\"\"
        prompt = f\"\"\"You are a resume parsing and structuring engine.

Extract and convert the following resume into structured JSON.

Rules:
- Do NOT lose any information
- Preserve ALL experience, responsibilities, and technologies
- Group content into sections:
  - name
  - title
  - summary
  - experience (role, company, client, dates, responsibilities, technologies)
  - skills
  - certifications
  - education
  - projects

Return ONLY valid JSON, with no markdown formatting or code blocks.

Resume:
{resume_text}\"\"\"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=600,
                max_tokens=8000,
            )
            response_text = completion.choices[0].message.content.strip()

            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"Local AI Error during Parsing: {str(e)}")

    def map_to_template(self, parsed_resume: Dict[str, Any],
                       template_structure: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Map parsed resume to template structure.
        \"\"\"
        prompt = f\"\"\"You are a resume formatter.

You are given:
1. Parsed resume JSON
2. Reference template structure

Your task:
- Map resume content EXACTLY into the reference structure
- Do NOT remove or summarize content
- Maintain all responsibilities and details
- Ensure sections align with the template sections
- Preserve exact formatting and order

Parsed Resume:
{json.dumps(parsed_resume, indent=2)}

Reference Template Structure:
{json.dumps(template_structure, indent=2)}

Return ONLY valid JSON with the resume mapped to the template structure, with no markdown formatting or code blocks.\"\"\"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=600,
                max_tokens=8000,
            )
            response_text = completion.choices[0].message.content.strip()

            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"Local AI Error during Template Mapping: {str(e)}")

    def suggest_improvements(self, resume_text: str) -> Dict[str, Any]:
        \"\"\"
        Generate ATS-friendly suggestions for resume improvement.
        \"\"\"
        prompt = f\"\"\"You are a resume improvement advisor.

Analyze the following resume and provide suggestions for:
1. ATS (Applicant Tracking System) optimization
2. Keyword optimization
3. Formatting improvements
4. Content clarity

Resume:
{resume_text}

Return ONLY valid JSON with suggestions, with no markdown formatting or code blocks.\"\"\"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=600,
                max_tokens=8000,
            )
            response_text = completion.choices[0].message.content.strip()

            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"Local AI Error during Suggestions: {str(e)}")
'''
with open(r'B:\Resume-Formatter\backend\gemini_service.py', 'w', encoding='utf-8') as f:
    f.write(content)