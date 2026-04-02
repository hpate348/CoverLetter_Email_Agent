# tools/parse_resume.py
import anthropic, json, re


client = anthropic.Anthropic()

def extract_highlights(resume_text: str, jd_summary: dict) -> list:
    required = ", ".join(jd_summary.get("required_skills", []))
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="You extract the most relevant resume bullets for a specific role. Return only valid JSON.",
        messages=[{
            "role": "user",
            "content": f"""Given this resume and required skills [{required}],
            return the 4 most relevant experiences or achievements as a JSON list of strings.
            Each should be a single punchy bullet. Do not fabricate anything.

            Resume:
            {resume_text}

            Return JSON array only."""
                    }]
                )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw.strip())