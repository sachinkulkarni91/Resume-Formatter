import json
import re
from openai import OpenAI
from config import GROQ_API_KEY, GROQ_MODEL
from typing import Dict, Any
from json_repair import repair_json


class GeminiService:
    """Service for interacting with Groq cloud API via OpenAI-compatible client."""

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY,
        )
        self.model = GROQ_MODEL
        # Truncate resume text to stay well under Groq free-tier ~12k TPM limit.
        # 4000 chars ≈ ~1000 tokens of input, leaving room for prompt + output.
        self.max_resume_chars = 4000

    def _truncate(self, text: str) -> str:
        """Trim text so total prompt stays within Groq free-tier TPM limits."""
        if len(text) > self.max_resume_chars:
            return text[:self.max_resume_chars] + "\n...[content truncated to fit token limit]"
        return text

    def _extract_and_parse_json(self, response_text: str) -> Dict[str, Any]:
        """Parse model output, repairing malformed JSON when possible."""
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
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
                raise ValueError(
                    f"CRITICAL: Failed to parse or repair LLM response. "
                    f"Error: {e}\nPreview: {response_text[:200]}..."
                )

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Parse resume text into structured JSON using Groq LLM."""
        prompt = f"""You are a resume parsing engine. Extract the resume below into structured JSON.

Return ONLY valid JSON with these fields:
{{
  "name": "", "title": "", "summary": "",
  "experience": [{{"role":"","company":"","client":"","dates":"","responsibilities":[],"technologies":[]}}],
  "skills": [], "certifications": [], "education": [], "projects": []
}}

Resume:
{self._truncate(resume_text)}"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=60,
                max_tokens=2000,
                response_format={"type": "json_object"},
            )
            response_text = completion.choices[0].message.content.strip()
            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"Groq API Error during Parsing: {str(e)}")

    def map_to_template(self, parsed_resume: Dict[str, Any],
                        template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skip the LLM call — pass parsed resume directly to the doc generator.
        The second LLM call was responsible for ALL the 413 token-limit errors
        because it sent the full parsed JSON + full template JSON combined.
        The doc_generator already handles layout from the parsed structure.
        """
        return parsed_resume

    def suggest_improvements(self, resume_text: str) -> Dict[str, Any]:
        """Generate ATS-friendly suggestions for resume improvement."""
        prompt = f"""You are a resume advisor. Analyze the resume below and return JSON with:
{{
  "ats_score": 0-100,
  "suggestions": [],
  "keywords_to_add": [],
  "formatting_tips": []
}}

Resume:
{self._truncate(resume_text)}"""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=60,
                max_tokens=1500,
                response_format={"type": "json_object"},
            )
            response_text = completion.choices[0].message.content.strip()
            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"Groq API Error during Suggestions: {str(e)}")
