# schemas.py
from pydantic import BaseModel

class AgentInput(BaseModel):
    company_name: str
    job_description: str
    resume_text: str        # pre-extracted from PDF at upload time
    user_name: str
    user_email: str

class AgentOutput(BaseModel):
    company_research: str
    jd_summary: dict        # {"required_skills": [...], "role_summary": "..."}
    resume_highlights: list # top 3-5 relevant experiences
    cover_letter: str
    outreach_email: str
    steps_taken: list       # full trace for the UI