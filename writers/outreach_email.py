# writers/outreach_email.py
import anthropic

client = anthropic.Anthropic()

SYSTEM = """You write short, direct cold outreach emails that get replies. 
No fluff. Lead with something specific about the company. 
End with one clear, low-friction ask."""

def write_outreach_email(
    user_name: str,
    user_email: str,
    company_name: str,
    jd_summary: dict,
    resume_highlights: list,
    company_research: str
) -> str:
    top_highlight = resume_highlights[0] if resume_highlights else ""

    prompt = f"""Write a cold outreach email from {user_name} ({user_email}) 
to a hiring manager or recruiter at {company_name}.

They're applying for: {jd_summary.get('role_title', 'an open role')}
Their strongest relevant achievement: {top_highlight}

Company context (pick ONE specific detail to open with):
{company_research[:400]}

Format:
Subject: [subject line]

[email body]

Instructions:
- Subject line under 8 words
- Body under 120 words
- Open with a specific, genuine observation about {company_name}
- One sentence on who they are and why relevant
- One sentence on the specific achievement
- Close with a single yes/no question ask (e.g. 'Would a 20-min call make sense?')
- Sign off with name and email"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text