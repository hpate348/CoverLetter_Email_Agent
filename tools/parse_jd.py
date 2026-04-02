# tools/parse_jd.py
import anthropic, json, re

client = anthropic.Anthropic()

def parse_jd(job_description: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="Extract structured data from job descriptions. Return only valid JSON.",
        messages=[{
            "role": "user",
            "content": f"""Extract from this JD:
- role_title
- required_skills (list)
- nice_to_have (list)
- role_summary (2 sentences max)
- company_values (if mentioned)

JD:
{job_description}

Return JSON only."""
        }]
    )
    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw.strip())