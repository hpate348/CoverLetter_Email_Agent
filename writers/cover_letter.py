# writers/cover_letter.py
import anthropic

client = anthropic.Anthropic()

SYSTEM = """You are an expert career coach who writes compelling, 
specific cover letters. Never use generic filler phrases like 
'I am excited to apply'. Every sentence must reference either 
the specific company, the specific role, or a specific achievement."""

def write_cover_letter(
    user_name: str,
    company_name: str,
    jd_summary: dict,
    resume_highlights: list,
    company_research: str
) -> str:
    highlights_text = "\n".join(f"- {h}" for h in resume_highlights)
    skills = ", ".join(jd_summary.get("required_skills", []))

    prompt = f"""Write a professional cover letter for {user_name} applying to 
{company_name} for the role of {jd_summary.get('role_title', 'this position')}.

Company research (use this to show genuine interest):
{company_research[:800]}

Role requires: {skills}

Candidate's most relevant experience:
{highlights_text}

Instructions:
- 3 paragraphs, under 350 words total
- Paragraph 1: Why this company specifically (use the research)
- Paragraph 2: Why they're qualified (use the highlights)  
- Paragraph 3: Specific ask + forward-looking close
- Professional but not stiff — write like a confident person, not a template
- Do NOT use: 'I am writing to', 'I am excited', 'passion for'"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text