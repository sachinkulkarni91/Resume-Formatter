import json
import re
import requests
from config import GROQ_API_KEY, GROQ_MODEL, LLM_PROVIDER, OLLAMA_MODEL, GEMINI_API_KEY, GEMINI_MODEL
from typing import Dict, Any, List
from json_repair import repair_json
import os

class GeminiService:
    """Service for LLM-based resume parsing.
    
    Supports three backends:
      - GEMINI: Google Gemini API via REST (High speed, massive context)
      - LOCAL: Ollama running on localhost (free, no API key needed)
      - CLOUD: Groq cloud API (requires API key, has rate limits)
    """

    def __init__(self):
        self.provider = LLM_PROVIDER

        if self.provider == "gemini":
            self.api_key = GEMINI_API_KEY
            self.model = GEMINI_MODEL
            self.max_resume_chars = 1000000 
            self.timeout = 60
            print(f"[CLOUD] Using Google Gemini REST API: {self.model}")

        elif self.provider == "ollama":
            from openai import OpenAI
            self.client = OpenAI(
                base_url="http://localhost:11434/v1",
                api_key="ollama",
            )
            self.model = OLLAMA_MODEL
            self.max_resume_chars = 30000
            self.timeout = 900
            print(f"[LOCAL] Using Ollama LLM: {self.model}")
            
        else:
            from openai import OpenAI
            self.client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=GROQ_API_KEY,
            )
            self.model = GROQ_MODEL
            self.max_resume_chars = 12000
            self.timeout = 60
            print(f"[CLOUD] Using Groq LLM: {self.model}")

    def _truncate(self, text: str) -> str:
        if len(text) > self.max_resume_chars:
            return text[:self.max_resume_chars] + "\n...[content truncated]"
        return text

    def _max_tokens_for(self, task: str) -> int:
        """Return provider-safe max output token budget per task."""
        if self.provider == "groq":
            # Groq on-demand tier has strict TPM; keep outputs conservative.
            if task == "parse":
                return 1800
            if task == "recover":
                return 1200
            if task == "experience":
                return 1500
            return 1000

        # Gemini/Ollama can use larger budgets.
        if task == "parse":
            return 12000
        if task == "recover":
            return 6000
        if task == "experience":
            return 12000
        return 4000

    def _extract_and_parse_json(self, response_text: str) -> Dict[str, Any]:
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
                raise ValueError(f"CRITICAL: Failed to parse LLM response. Error: {e}")

    def _create_completion(self, prompt: str, max_tokens: int = 4000) -> str:
        if self.provider == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "maxOutputTokens": max_tokens
                }
            }
            response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            response.raise_for_status()
            
            # Extract text from Gemini REST payload
            resp_json = response.json()
            if "candidates" in resp_json and len(resp_json["candidates"]) > 0:
                parts = resp_json["candidates"][0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            raise Exception("Gemini API returned an empty response")

        else:
            kwargs = dict(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                timeout=self.timeout,
                max_tokens=max_tokens,
            )
            if self.provider == "groq":
                kwargs["response_format"] = {"type": "json_object"}

            completion = self.client.chat.completions.create(**kwargs)
            return completion.choices[0].message.content.strip()

    def _is_empty_section(self, value: Any) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, (list, dict, tuple, set)):
            return len(value) == 0
        return False

    def _find_missing_sections(self, parsed_resume: Dict[str, Any]) -> list:
        required_sections = [
            "name",
            "title",
            "summary",
            "experience",
            "skills",
            "certifications",
            "education",
        ]
        missing = []
        for section in required_sections:
            if section not in parsed_resume or self._is_empty_section(parsed_resume.get(section)):
                missing.append(section)
        return missing

    def _merge_missing_sections(self, base: Dict[str, Any], supplement: Dict[str, Any], missing_sections: list) -> Dict[str, Any]:
        merged = dict(base)
        for section in missing_sections:
            value = supplement.get(section)
            if not self._is_empty_section(value):
                merged[section] = value
        return merged

        def _count_experience_detail(self, experience: Any) -> int:
                """Rough completeness score for experience richness."""
                if not isinstance(experience, list):
                        return 0

                score = 0
                for exp in experience:
                        if not isinstance(exp, dict):
                                continue

                        # Base role entry
                        score += 1

                        responsibilities = exp.get("responsibilities", [])
                        if isinstance(responsibilities, list):
                                score += len(responsibilities)

                        projects = exp.get("projects", [])
                        if isinstance(projects, list):
                                score += len(projects) * 2
                                for p in projects:
                                        if not isinstance(p, dict):
                                                continue
                                        pr = p.get("responsibilities", [])
                                        if isinstance(pr, list):
                                                score += len(pr)
                return score

        def _extract_experience_only(self, resume_text: str) -> List[Dict[str, Any]]:
                prompt = f"""Extract ONLY complete professional experience from this resume.

Rules:
1) Return ONLY valid JSON.
2) JSON must have exactly one top-level key: "experience".
3) Include ALL roles, ALL projects, ALL responsibilities, ALL technologies, ALL dates.
4) Do NOT summarize or shorten any bullet points.

Return format:
{{
    "experience": [
        {{
            "role": "",
            "company": "",
            "client": "",
            "dates": "",
            "responsibilities": [""],
            "technologies": [""],
            "projects": [
                {{
                    "name": "",
                    "client": "",
                    "dates": "",
                    "description": "",
                    "technologies": [""],
                    "responsibilities": [""]
                }}
            ]
        }}
    ]
}}

Resume:
{self._truncate(resume_text)}"""

                response_text = self._create_completion(prompt, max_tokens=self._max_tokens_for("experience"))
                parsed = self._extract_and_parse_json(response_text)
                experience = parsed.get("experience", []) if isinstance(parsed, dict) else []
                return experience if isinstance(experience, list) else []

            def _is_groq_too_large_error(self, exc: Exception) -> bool:
                msg = str(exc).lower()
                return self.provider == "groq" and (
                    "request too large" in msg
                    or "tokens per minute" in msg
                    or "rate_limit_exceeded" in msg
                    or "error code: 413" in msg
                )

    def _recover_missing_sections(self, resume_text: str, missing_sections: list) -> Dict[str, Any]:
        section_list = ", ".join(f'"{s}"' for s in missing_sections)
        prompt = f"""You previously returned incomplete resume JSON.

Extract ONLY the missing sections from the resume below and return valid JSON.

Rules:
1) Return ONLY a JSON object.
2) Include ONLY these keys: {section_list}
3) Copy all relevant details exactly; do not summarize or omit details.

Resume:
{self._truncate(resume_text)}"""

        response_text = self._create_completion(prompt, max_tokens=self._max_tokens_for("recover"))
        recovered = self._extract_and_parse_json(response_text)
        return recovered if isinstance(recovered, dict) else {}

    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        """Parse resume text into structured JSON using the configured LLM."""
        prompt = f"""You are a resume parsing engine. Extract ALL information from the resume below into structured JSON.

IMPORTANT: Extract EVERY SINGLE responsibility, project, date, technology, and line of experience from the resume. Do NOT skip, condense, or summarize ANY content. The output MUST contain 100% of the original bullet points unedited. If the resume is 7 pages, extract 7 pages worth of detail!

CRITICAL: You MUST return a complete JSON object containing "name", "title", "summary", "experience", "skills", "certifications", and "education". DO NOT merge the experience into the summary. Keep all sections strictly separated into the correct JSON fields!

Return ONLY valid JSON with these fields:
{{
  "name": "",
  "title": "",
  "summary": "String containing the EXACT full professional summary and ALL bullet points combined into one paragraph without skipping any words.",
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
{self._truncate(resume_text)}"""

        try:
            response_text = self._create_completion(prompt, max_tokens=self._max_tokens_for("parse"))
            parsed_resume = self._extract_and_parse_json(response_text)

            if not isinstance(parsed_resume, dict):
                parsed_resume = {}

            missing_sections = self._find_missing_sections(parsed_resume)
            if missing_sections:
                print(f"[WARN] Incomplete LLM output. Missing sections: {missing_sections}")
                recovered = self._recover_missing_sections(resume_text, missing_sections)
                parsed_resume = self._merge_missing_sections(parsed_resume, recovered, missing_sections)

            # Enrich experience in a dedicated pass for long resumes where first pass may truncate.
            try:
                enriched_experience = self._extract_experience_only(resume_text)
                current_score = self._count_experience_detail(parsed_resume.get("experience", []))
                enriched_score = self._count_experience_detail(enriched_experience)
                if enriched_score > current_score:
                    print(f"[INFO] Replaced experience with richer extraction ({current_score} -> {enriched_score}).")
                    parsed_resume["experience"] = enriched_experience
            except Exception as enrich_error:
                print(f"[WARN] Experience enrichment skipped: {enrich_error}")

            # Final safety net: ensure all expected keys exist so generator always renders sections consistently.
            for k, default in {
                "name": "",
                "title": "",
                "summary": "",
                "experience": [],
                "skills": [],
                "certifications": [],
                "education": [],
            }.items():
                if k not in parsed_resume:
                    parsed_resume[k] = default

            return parsed_resume
        except Exception as e:
            if self._is_groq_too_large_error(e):
                # Retry with a smaller input slice and lower output budget for strict Groq limits.
                try:
                    retry_chars = min(5000, len(resume_text))
                    reduced_resume = resume_text[:retry_chars]
                    retry_prompt = f"""You are a resume parsing engine. Extract structured JSON from this resume content.

Return ONLY valid JSON with keys: name, title, summary, experience, skills, certifications, education.
Keep fields concise if needed, but preserve key role/company/date/project/responsibility details.

Resume:
{reduced_resume}"""
                    response_text = self._create_completion(retry_prompt, max_tokens=1200)
                    parsed_resume = self._extract_and_parse_json(response_text)
                    if isinstance(parsed_resume, dict):
                        for k, default in {
                            "name": "",
                            "title": "",
                            "summary": "",
                            "experience": [],
                            "skills": [],
                            "certifications": [],
                            "education": [],
                        }.items():
                            if k not in parsed_resume:
                                parsed_resume[k] = default
                        return parsed_resume
                except Exception:
                    pass

            raise Exception(f"LLM Error during Parsing ({self.provider}): {str(e)}")

    def map_to_template(self, parsed_resume: Dict[str, Any],
                        template_structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skip the LLM call — pass parsed resume directly to the doc generator.
        """
        return parsed_resume

    def suggest_improvements(self, resume_text: str) -> Dict[str, Any]:
        """Generate ATS-friendly suggestions for resume improvement."""
        prompt = f"""You are a resume advisor. Analyze the resume below and return ONLY valid JSON with:
{{
  "ats_score": "0-100",
  "suggestions": ["suggestion1", "suggestion2"],
  "keywords_to_add": ["keyword1", "keyword2"],
  "formatting_tips": ["tip1", "tip2"]
}}

Resume:
{self._truncate(resume_text)}"""

        try:
            response_text = self._create_completion(prompt, max_tokens=2000)
            return self._extract_and_parse_json(response_text)
        except Exception as e:
            raise Exception(f"LLM Error during Suggestions ({self.provider}): {str(e)}")
