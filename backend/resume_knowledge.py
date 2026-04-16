import json
import os
import re
from typing import Any, Dict, List


class ResumeKnowledgeBase:
    """Tiny JSONL-backed knowledge base for prior parsed resumes."""

    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def _tokenize(self, text: str) -> set:
        return set(re.findall(r"[a-z0-9]+", (text or "").lower()))

    def _similarity(self, a: str, b: str) -> float:
        ta = self._tokenize(a)
        tb = self._tokenize(b)
        if not ta or not tb:
            return 0.0
        inter = len(ta.intersection(tb))
        union = len(ta.union(tb))
        return inter / union if union else 0.0

    def _read_entries(self, limit: int = 200) -> List[Dict[str, Any]]:
        if not os.path.exists(self.path):
            return []
        entries: List[Dict[str, Any]] = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entries.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            return []
        return entries[-limit:]

    def _to_hint(self, parsed: Dict[str, Any]) -> str:
        name = parsed.get("name", "")
        title = parsed.get("title", "")
        skills = parsed.get("skills", [])
        exp = parsed.get("experience", [])
        skill_count = len(skills) if isinstance(skills, list) else 0
        exp_count = len(exp) if isinstance(exp, list) else 0
        return f"name={name}; title={title}; experience_count={exp_count}; skills_count={skill_count}"

    def get_context(self, resume_text: str, top_k: int = 3) -> str:
        entries = self._read_entries()
        if not entries:
            return ""

        scored = []
        for e in entries:
            score = self._similarity(resume_text, e.get("resume_text", ""))
            if score > 0:
                scored.append((score, e))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_k]
        if not top:
            return ""

        hints = []
        for i, (_, e) in enumerate(top, start=1):
            parsed = e.get("parsed_resume", {})
            if isinstance(parsed, dict):
                hints.append(f"Example {i}: {self._to_hint(parsed)}")

        return "\n".join(hints)

    def add_entry(self, resume_text: str, parsed_resume: Dict[str, Any]) -> None:
        record = {
            "resume_text": (resume_text or "")[:5000],
            "parsed_resume": parsed_resume if isinstance(parsed_resume, dict) else {},
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=True) + "\n")
