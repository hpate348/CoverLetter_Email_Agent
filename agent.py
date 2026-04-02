# agent.py
from tools.search import search_company
from tools.parse_jd import parse_jd
from tools.parse_resume import extract_highlights
from writers.cover_letter import write_cover_letter
from writers.outreach_email import write_outreach_email
from schemas import AgentInput, AgentOutput

def run(input: AgentInput) -> AgentOutput:
    steps = []

    # Step 1: Parse the JD
    steps.append({"step": "Parsing job description...", "status": "running"})
    jd_summary = parse_jd(input.job_description)
    steps[-1]["status"] = "done"
    steps[-1]["result"] = jd_summary

    # Step 2: Research the company
    steps.append({"step": f"Researching {input.company_name}...", "status": "running"})
    company_research = search_company(input.company_name)
    steps[-1]["status"] = "done"
    steps[-1]["result"] = company_research[:200] + "..."

    # Step 3: Match resume to JD
    steps.append({"step": "Matching resume to role...", "status": "running"})
    resume_highlights = extract_highlights(input.resume_text, jd_summary)
    steps[-1]["status"] = "done"
    steps[-1]["result"] = resume_highlights

    # Step 4: Write cover letter
    steps.append({"step": "Writing cover letter...", "status": "running"})
    cover_letter = write_cover_letter(
        user_name=input.user_name,
        company_name=input.company_name,
        jd_summary=jd_summary,
        resume_highlights=resume_highlights,
        company_research=company_research
    )
    steps[-1]["status"] = "done"

    # Step 5: Write outreach email
    steps.append({"step": "Writing outreach email...", "status": "running"})
    outreach_email = write_outreach_email(
        user_name=input.user_name,
        user_email=input.user_email,
        company_name=input.company_name,
        jd_summary=jd_summary,
        resume_highlights=resume_highlights,
        company_research=company_research
    )
    steps[-1]["status"] = "done"

    return AgentOutput(
        company_research=company_research,
        jd_summary=jd_summary,
        resume_highlights=resume_highlights,
        cover_letter=cover_letter,
        outreach_email=outreach_email,
        steps_taken=steps
    )