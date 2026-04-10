from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import Dict, Any, List
import copy


class DocxGenerator:
    """Generator for creating formatted DOCX documents"""

    def __init__(self, template_path: str = None):
        """
        Initialize document generator.
        
        Args:
            template_path: Optional path to template document
        """
        if template_path:
            self.template_doc = Document(template_path)
            self.doc = copy.deepcopy(self.template_doc)
            self.template_style_sequence = self._extract_template_style_sequence()
            self.name_style = self._style_or_fallback(0, "Normal")
            self.title_style = self._style_or_fallback(1, self.name_style)
            self.heading_style = self._style_or_fallback(2, self.title_style)
            self.body_style = self._style_or_fallback(3, self.heading_style)
            self.list_style = self._style_or_fallback(4, self.body_style)
        else:
            self.doc = Document()
            self.template_style_sequence = []
            self.name_style = "Normal"
            self.title_style = "Normal"
            self.heading_style = "Normal"
            self.body_style = "Normal"
            self.list_style = "Normal"
        
        self.template_path = template_path

    def _extract_template_style_sequence(self) -> List[str]:
        """Get paragraph style names from the reference template in document order."""
        styles = []
        for para in self.template_doc.paragraphs:
            style_name = getattr(para.style, "name", None)
            if style_name and style_name not in styles:
                styles.append(style_name)
        return styles

    def _style_or_fallback(self, index: int, fallback: str) -> str:
        """Return a template style name if available and valid in the document."""
        if 0 <= index < len(self.template_style_sequence):
            candidate = self.template_style_sequence[index]
            try:
                _ = self.doc.styles[candidate]
                return candidate
            except Exception:
                return fallback
        return fallback

    def _safe_set_style(self, para, style_name: str) -> bool:
        """
        Safely set paragraph style, falling back to Normal if style doesn't exist.
        
        Args:
            para: Paragraph to set style on
            style_name: Name of style to apply
            
        Returns:
            True if style was applied, False if fallback to Normal was used
        """
        try:
            para.style = style_name
            return True
        except Exception:
            try:
                para.style = "Normal"
                return False
            except Exception:
                # If style resolution fails entirely, keep the paragraph default style.
                return False

    def generate_from_structured_data(self, data: Dict[str, Any]) -> Document:
        """
        Generate document from structured resume data.
        
        Args:
            data: Structured resume data
            
        Returns:
            Generated Document
        """
        # Clear template paragraphs if using template
        if self.template_path:
            # Keep only template structure, we'll modify content
            self.doc = copy.deepcopy(self.template_doc)
            
            # Actually remove all existing paragraphs from the copied template document
            for para in self.doc.paragraphs:
                p = para._element
                p.getparent().remove(p)
                
            # Remove any tables as well
            for table in self.doc.tables:
                t = table._element
                t.getparent().remove(t)

        # Generate sections
        if "name" in data:
            self._add_name_section(data.get("name", ""))
        
        if "title" in data:
            self._add_title_section(data.get("title", ""))
        
        if "summary" in data and data["summary"]:
            self._add_section("PROFESSIONAL SUMMARY", data["summary"])
        
        if "experience" in data and data["experience"]:
            self._add_experience_section(data["experience"])
        
        if "skills" in data and data["skills"]:
            self._add_skills_section(data["skills"])
        
        if "certifications" in data and data["certifications"]:
            self._add_certifications_section(data["certifications"])
        
        if "education" in data and data["education"]:
            self._add_education_section(data["education"])
        
        if "projects" in data and data["projects"]:
            self._add_projects_section(data["projects"])

        return self.doc

    def _add_name_section(self, name: str):
        """Add name as heading"""
        para = self.doc.add_paragraph()
        self._safe_set_style(para, self.name_style)
        run = para.add_run(name)
        run.font.size = Pt(16)
        run.font.bold = True

    def _add_title_section(self, title: str):
        """Add professional title"""
        para = self.doc.add_paragraph(title)
        self._safe_set_style(para, self.title_style)
        for run in para.runs:
            run.font.size = Pt(12)
            run.font.italic = True

    def _add_section(self, section_name: str, content: Any):
        """
        Add a generic section.
        
        Args:
            section_name: Section heading
            content: Section content (string or list)
        """
        # Heading
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run(section_name)
        run.font.bold = True
        run.font.size = Pt(12)

        # Content
        if isinstance(content, str):
            para = self.doc.add_paragraph(content)
            self._safe_set_style(para, self.body_style)
        elif isinstance(content, list):
            for item in content:
                item_para = self.doc.add_paragraph(item)
                self._safe_set_style(item_para, self.list_style)

    def _add_experience_section(self, experience: List[Dict[str, Any]]):
        """Add professional experience section"""
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run("PROFESSIONAL EXPERIENCE")
        run.font.bold = True
        run.font.size = Pt(12)

        for job in experience:
            # Role and Company
            job_title = job.get("role", "")
            company = job.get("company", "")
            
            job_para = self.doc.add_paragraph()
            self._safe_set_style(job_para, self.list_style)
            
            job_run = job_para.add_run(f"{job_title} at {company}")
            job_run.font.bold = True
            job_run.font.size = Pt(11)

            # Dates
            dates = job.get("dates", "")
            if dates:
                dates_para = self.doc.add_paragraph(dates)
                self._safe_set_style(dates_para, self.body_style)
                dates_para.paragraph_format.left_indent = Inches(0.25)

            # Responsibilities
            responsibilities = job.get("responsibilities", [])
            if isinstance(responsibilities, list):
                for responsibility in responsibilities:
                    resp_para = self.doc.add_paragraph(responsibility)
                    self._safe_set_style(resp_para, self.list_style)
                    resp_para.paragraph_format.left_indent = Inches(0.5)
            elif isinstance(responsibilities, str) and responsibilities:
                resp_para = self.doc.add_paragraph(responsibilities)
                self._safe_set_style(resp_para, self.list_style)
                resp_para.paragraph_format.left_indent = Inches(0.5)

            # Technologies
            technologies = job.get("technologies", [])
            if technologies:
                if isinstance(technologies, list):
                    tech_text = ", ".join(technologies)
                else:
                    tech_text = str(technologies)
                
                tech_para = self.doc.add_paragraph(f"Technologies: {tech_text}")
                self._safe_set_style(tech_para, self.body_style)
                tech_para.paragraph_format.left_indent = Inches(0.25)
                for run in tech_para.runs:
                    run.font.italic = True
                    run.font.size = Pt(10)

    def _add_skills_section(self, skills: Dict[str, List[str]] | List[str]):
        """Add skills section"""
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run("SKILLS")
        run.font.bold = True
        run.font.size = Pt(12)

        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                cat_para = self.doc.add_paragraph(f"{category}:")
                self._safe_set_style(cat_para, self.body_style)
                for run in cat_para.runs:
                    run.font.bold = True

                for skill in skill_list:
                    skill_para = self.doc.add_paragraph(skill)
                    self._safe_set_style(skill_para, self.list_style)

        elif isinstance(skills, list):
            for skill in skills:
                skill_para = self.doc.add_paragraph(skill)
                self._safe_set_style(skill_para, self.list_style)

    def _add_certifications_section(self, certifications: List[Dict[str, str]] | List[str]):
        """Add certifications section"""
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run("CERTIFICATIONS")
        run.font.bold = True
        run.font.size = Pt(12)

        if isinstance(certifications, list):
            for cert in certifications:
                if isinstance(cert, dict):
                    cert_text = f"{cert.get('name', '')} - {cert.get('issuer', '')} ({cert.get('date', '')})"
                else:
                    cert_text = str(cert)
                
                cert_para = self.doc.add_paragraph(cert_text)
                self._safe_set_style(cert_para, self.list_style)

    def _add_education_section(self, education: List[Dict[str, str]] | List[str]):
        """Add education section"""
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run("EDUCATION")
        run.font.bold = True
        run.font.size = Pt(12)

        if isinstance(education, list):
            for edu in education:
                if isinstance(edu, dict):
                    degree = edu.get("degree", "")
                    school = edu.get("school", "")
                    year = edu.get("year", "")
                    edu_text = f"{degree} from {school} ({year})"
                else:
                    edu_text = str(edu)
                
                edu_para = self.doc.add_paragraph(edu_text)
                self._safe_set_style(edu_para, self.list_style)

    def _add_projects_section(self, projects: List[Dict[str, Any]]):
        """Add projects section"""
        heading = self.doc.add_paragraph()
        self._safe_set_style(heading, self.heading_style)
        run = heading.add_run("PROJECTS")
        run.font.bold = True
        run.font.size = Pt(12)

        for project in projects:
            # Project title
            proj_title = project.get("title", "")
            proj_para = self.doc.add_paragraph(proj_title)
            self._safe_set_style(proj_para, self.list_style)
            for run in proj_para.runs:
                run.font.bold = True

            # Description
            description = project.get("description", "")
            if description:
                desc_para = self.doc.add_paragraph(description)
                self._safe_set_style(desc_para, self.body_style)
                desc_para.paragraph_format.left_indent = Inches(0.25)

            # Technologies
            technologies = project.get("technologies", [])
            if technologies:
                if isinstance(technologies, list):
                    tech_text = ", ".join(technologies)
                else:
                    tech_text = str(technologies)
                
                tech_para = self.doc.add_paragraph(f"Tech: {tech_text}")
                self._safe_set_style(tech_para, self.body_style)
                tech_para.paragraph_format.left_indent = Inches(0.25)
                for run in tech_para.runs:
                    run.font.italic = True
                    run.font.size = Pt(10)

    def save(self, output_path: str):
        """
        Save document to file.
        
        Args:
            output_path: Path to save DOCX file
        """
        try:
            self.doc.save(output_path)
        except Exception as e:
            raise Exception(f"Error saving document: {e}")
