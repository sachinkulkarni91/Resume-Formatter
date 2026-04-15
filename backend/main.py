from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import json
from typing import Optional
import shutil

from config import API_HOST, API_PORT, UPLOAD_DIR, OUTPUT_DIR, MAX_FILE_SIZE, CORS_ORIGINS, ALLOWED_EXTENSIONS
from parser import ResumeParser, TemplateParser
from gemini_service import GeminiService
from template_engine import TemplateEngine
from doc_generator import DocxGenerator

# Initialize FastAPI
app = FastAPI(
    title="Resume Formatter API",
    description="Convert resumes to template format using Gemini AI",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_service = GeminiService()

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def cleanup_file(file_path: str):
    """Clean up uploaded file after processing"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error cleaning up file: {e}")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Resume Formatter API",
        "version": "1.0.0"
    }


@app.post("/api/format-resume")
async def format_resume(
    target_resume: UploadFile = File(...),
    template: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Format a resume to match template structure.
    
    Parameters:
    - target_resume: The resume to be formatted
    - template: The reference template
    
    Returns:
    - Formatted DOCX file
    """
    
    temp_target_path = None
    temp_template_path = None
    output_file = None
    
    try:
        # Validate file types
        target_ext = os.path.splitext(target_resume.filename)[1].lower().lstrip(".")
        template_ext = os.path.splitext(template.filename)[1].lower().lstrip(".")
        
        if target_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid target resume format: {target_ext}"
            )
        
        if template_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid template format: {template_ext}"
            )

        # Save uploaded files
        request_id = str(uuid.uuid4())
        temp_target_path = os.path.join(UPLOAD_DIR, f"{request_id}_target_{target_resume.filename}")
        temp_template_path = os.path.join(UPLOAD_DIR, f"{request_id}_template_{template.filename}")
        
        with open(temp_target_path, "wb") as f:
            f.write(await target_resume.read())
        
        with open(temp_template_path, "wb") as f:
            f.write(await template.read())

        # Parse target resume
        print(f"Parsing target resume: {temp_target_path}")
        resume_text = ResumeParser.parse(temp_target_path)
        
        # Parse template
        print(f"Extracting template structure: {temp_template_path}")
        template_info = TemplateParser.extract_template_info(temp_template_path)

        # Use Gemini to structure resume
        print("Using Gemini to parse resume...")
        parsed_resume = gemini_service.parse_resume(resume_text)

        # DEBUG: Print parsed resume name
        import json
        print(f"DEBUG PARSED NAME: {parsed_resume.get('name', 'NO NAME FOUND')}")
        print(f"DEBUG PARSED KEYS: {list(parsed_resume.keys())}")

        # Map to template using Gemini
        print("Mapping resume to template...")
        template_structure = {
            "sections": template_info.get("sections", []),
            "styles": template_info.get("styles", {}),
            "margins": template_info.get("margins", {})
        }
        
        mapped_resume = gemini_service.map_to_template(parsed_resume, template_structure)

        # Generate formatted DOCX
        print("Generating formatted document...")
        generator = DocxGenerator(temp_template_path)
        formatted_doc = generator.generate_from_structured_data(mapped_resume)

        # Save output
        output_file = os.path.join(OUTPUT_DIR, f"{request_id}_formatted.docx")
        formatted_doc.save(output_file)
        # Schedule cleanup
        if background_tasks:
            background_tasks.add_task(cleanup_file, temp_target_path)
            background_tasks.add_task(cleanup_file, temp_template_path)

        return FileResponse(
            output_file,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="formatted_resume.docx"
        )

    except HTTPException as e:
        # Clean up on error
        if temp_target_path:
            cleanup_file(temp_target_path)
        if temp_template_path:
            cleanup_file(temp_template_path)
        if output_file:
            cleanup_file(output_file)
        raise e

    except Exception as e:
        import traceback
        traceback.print_exc()
        # Clean up on error
        if temp_target_path:
            cleanup_file(temp_target_path)
        if temp_template_path:
            cleanup_file(temp_template_path)
        if output_file:
            cleanup_file(output_file)
            
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the resume: {str(e)}\n\n{traceback.format_exc()}"
        )


@app.post("/api/format-from-parsed")
async def format_from_parsed(
    parsed_json: str = Form(...),
    template: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    """
    Generate formatted resume directly from reviewed parsed JSON and template.

    Parameters:
    - parsed_json: Structured resume JSON as string
    - template: The reference template

    Returns:
    - Formatted DOCX file
    """
    temp_template_path = None
    output_file = None

    try:
        template_ext = os.path.splitext(template.filename)[1].lower().lstrip(".")
        if template_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid template format: {template_ext}",
            )

        try:
            mapped_resume = json.loads(parsed_json)
            if not isinstance(mapped_resume, dict):
                raise ValueError("parsed_json must be a JSON object")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid parsed_json: {str(e)}")

        request_id = str(uuid.uuid4())
        temp_template_path = os.path.join(UPLOAD_DIR, f"{request_id}_template_{template.filename}")

        with open(temp_template_path, "wb") as f:
            f.write(await template.read())

        print("Generating formatted document from reviewed parsed JSON...")
        generator = DocxGenerator(temp_template_path)
        formatted_doc = generator.generate_from_structured_data(mapped_resume)

        output_file = os.path.join(OUTPUT_DIR, f"{request_id}_formatted.docx")
        formatted_doc.save(output_file)

        if background_tasks:
            background_tasks.add_task(cleanup_file, temp_template_path)

        return FileResponse(
            output_file,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="formatted_resume.docx",
        )

    except HTTPException as e:
        if temp_template_path:
            cleanup_file(temp_template_path)
        if output_file:
            cleanup_file(output_file)
        raise e

    except Exception as e:
        if temp_template_path:
            cleanup_file(temp_template_path)
        if output_file:
            cleanup_file(output_file)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating from parsed JSON: {str(e)}",
        )


@app.post("/api/parse-resume")
async def parse_resume_endpoint(resume: UploadFile = File(...)):
    """
    Parse a resume and return structured JSON.
    
    Parameters:
    - resume: Resume file (PDF or DOCX)
    
    Returns:
    - Structured resume JSON
    """
    temp_path = None
    
    try:
        ext = os.path.splitext(resume.filename)[1].lower().lstrip(".")
        
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {ext}"
            )

        # Save file
        request_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_DIR, f"{request_id}_{resume.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(await resume.read())

        # Parse
        resume_text = ResumeParser.parse(temp_path)
        parsed = gemini_service.parse_resume(resume_text)

        # Clean up
        cleanup_file(temp_path)

        return JSONResponse(parsed)

    except HTTPException as e:
        if temp_path:
            cleanup_file(temp_path)
        raise e

    except Exception as e:
        if temp_path:
            cleanup_file(temp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing resume: {str(e)}"
        )


@app.post("/api/extract-template")
async def extract_template_endpoint(template: UploadFile = File(...)):
    """
    Extract structure from template document.
    
    Parameters:
    - template: Template DOCX file
    
    Returns:
    - Template structure JSON
    """
    temp_path = None
    
    try:
        ext = os.path.splitext(template.filename)[1].lower().lstrip(".")
        
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {ext}"
            )

        # Save file
        request_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_DIR, f"{request_id}_{template.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(await template.read())

        # Extract template
        template_info = TemplateParser.extract_template_info(temp_path)

        # Clean up
        cleanup_file(temp_path)

        return JSONResponse(template_info)

    except HTTPException as e:
        if temp_path:
            cleanup_file(temp_path)
        raise e

    except Exception as e:
        if temp_path:
            cleanup_file(temp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting template: {str(e)}"
        )


@app.post("/api/suggest-improvements")
async def suggest_improvements_endpoint(resume: UploadFile = File(...)):
    """
    Get ATS optimization suggestions for a resume.
    
    Parameters:
    - resume: Resume file (PDF or DOCX)
    
    Returns:
    - Suggestions JSON
    """
    temp_path = None
    
    try:
        ext = os.path.splitext(resume.filename)[1].lower().lstrip(".")
        
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format: {ext}"
            )

        # Save file
        request_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_DIR, f"{request_id}_{resume.filename}")
        
        with open(temp_path, "wb") as f:
            f.write(await resume.read())

        # Extract text
        resume_text = ResumeParser.parse(temp_path)
        
        # Get suggestions
        suggestions = gemini_service.suggest_improvements(resume_text)

        # Clean up
        cleanup_file(temp_path)

        return JSONResponse(suggestions)

    except HTTPException as e:
        if temp_path:
            cleanup_file(temp_path)
        raise e

    except Exception as e:
        if temp_path:
            cleanup_file(temp_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestions: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT
    )
