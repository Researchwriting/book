import os
import threading
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from src.config import Config
from src.syllabus_parser import parse_syllabus
from src.progress_tracker import progress_tracker
from src.interactive_main import generate_section, get_generator

app = FastAPI(title="Textbook Generator API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (Frontend)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Global State
class AppState:
    def __init__(self):
        self.config = Config()
        self.generator = get_generator(self.config)
        self.is_generating = False
        self.current_section = None

state = AppState()

# Models
class Section(BaseModel):
    section_number: str
    section_title: str
    chapter: str
    status: str = "pending"

class GenerationRequest(BaseModel):
    section_number: str

# Endpoints

@app.get("/api/status")
def get_status():
    return {
        "is_generating": state.is_generating,
        "current_section": state.current_section,
        "model": state.config.MODEL_NAME
    }

@app.get("/api/sections")
def get_sections():
    if not os.path.exists("syllabus.md"):
        return []
    
    sections = parse_syllabus("syllabus.md")
    result = []
    for s in sections:
        # Check status
        filename = f"output/Section_{s['section_number']}_{s['section_title'].replace(' ', '_')}.md"
        status = "complete" if os.path.exists(filename) else "pending"
        
        result.append({
            "section_number": s['section_number'],
            "section_title": s['section_title'],
            "chapter": s['chapter'],
            "status": status
        })
    return result

@app.post("/api/generate/{section_number}")
def start_generation(section_number: str, background_tasks: BackgroundTasks):
    if state.is_generating:
        raise HTTPException(status_code=400, detail="Already generating a section")
    
    sections = parse_syllabus("syllabus.md")
    target_section = next((s for s in sections if s['section_number'] == section_number), None)
    
    if not target_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Start generation in background
    background_tasks.add_task(run_generation, target_section)
    
    return {"status": "started", "section": target_section['section_title']}

def run_generation(section_info):
    state.is_generating = True
    state.current_section = section_info['section_number']
    
    try:
        # We need to adapt generate_section to use progress_tracker if it doesn't already
        # For now, we assume it prints to stdout, but we want to capture that or use progress_tracker
        # Let's ensure progress_tracker is used in generate_section (we might need to patch it)
        
        # Find index
        sections = parse_syllabus("syllabus.md")
        idx = sections.index(section_info) + 1
        
        generate_section(state.generator, section_info, idx, len(sections))
        
    except Exception as e:
        print(f"Generation failed: {e}")
    finally:
        state.is_generating = False
        state.current_section = None

@app.get("/api/progress")
def get_progress():
    # Return data from progress_tracker
    return progress_tracker.sections

@app.get("/api/download/{section_number}")
def download_section(section_number: str):
    sections = parse_syllabus("syllabus.md")
    target_section = next((s for s in sections if s['section_number'] == section_number), None)
    
    if not target_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    filename = f"output/Section_{section_number}_{target_section['section_title'].replace(' ', '_')}.md"
    docx_filename = filename.replace('.md', '.docx')
    
    # Prefer DOCX if available
    if os.path.exists(docx_filename):
        return FileResponse(docx_filename, filename=os.path.basename(docx_filename))
    elif os.path.exists(filename):
        return FileResponse(filename, filename=os.path.basename(filename))
    else:
        raise HTTPException(status_code=404, detail="File not generated yet")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
