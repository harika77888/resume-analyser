from fastapi import FastAPI, uploadFile, File
import os
import uvicorn
import pdfplumber
from fastapi.middleware.cors import CORSMiddleware
from skills_data import job_roles
 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
@app.get("/")
def home():
    return {"message": "Resume Analyser backend is working!"}
 
 
@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.lower()
 
    found_skills = []
    for role, skills in job_roles.items():
        for skill in skills:
            if skill in text and skill not in found_skills:
                found_skills.append(skill)
 
    role_matches = []
    for role, required_skills in job_roles.items():
        matched = [s for s in required_skills if s in found_skills]
        if matched:
            match_percent = round((len(matched) / len(required_skills)) * 100)
            role_matches.append({
                "role": role,
                "matched_skills": matched,
                "match_percent": match_percent
            })
 
    role_matches.sort(key=lambda x: x["match_percent"], reverse=True)
 
    return {
        "skills_found": found_skills,
        "recommended_jobs": role_matches
    }
 }
if_name_=="_main_";
   port = int(os.environ.get("PORT",8000))
   uvicorn.run(app, host="0.0.0.0",port=port)