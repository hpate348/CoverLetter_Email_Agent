# main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pdfplumber, io, json, os
from agent import run
from schemas import AgentInput

app = FastAPI()

def extract_pdf_text(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

@app.post("/apply")
async def apply(
    company_name: str = Form(...),
    user_name: str = Form(...),
    user_email: str = Form(...),
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    resume_bytes = await resume.read()
    resume_text = extract_pdf_text(resume_bytes)

    agent_input = AgentInput(
        company_name=company_name,
        job_description=job_description,
        resume_text=resume_text,
        user_name=user_name,
        user_email=user_email
    )

    result = run(agent_input)

    # Save outputs to disk
    os.makedirs("outputs", exist_ok=True)
    slug = company_name.lower().replace(" ", "_")
    with open(f"outputs/{slug}_cover_letter.txt", "w") as f:
        f.write(result.cover_letter)
    with open(f"outputs/{slug}_outreach_email.txt", "w") as f:
        f.write(result.outreach_email)

    return JSONResponse(result.model_dump())