# Cover Letter & Outreach Email Agent

An AI agent that takes a job description and your resume, researches the company, then writes a tailored cover letter and cold outreach email — all in one click.

## How it works

The agent runs five steps in sequence:

1. **Parse JD** — extracts role title, required skills, and a summary from the job description
2. **Research company** — uses Tavily to pull recent news, culture, and mission context
3. **Match resume** — identifies your 4 most relevant experiences for this specific role
4. **Write cover letter** — 3-paragraph letter grounded in the company research and your highlights
5. **Write outreach email** — short cold email with a specific opener and a single clear ask

All writing is done via Claude (claude-sonnet-4-5). Nothing is fabricated — the agent only works with what you give it.

## Stack

- **Frontend** — Streamlit
- **Agent logic** — Python (`agent.py`)
- **LLM** — Anthropic Claude via `anthropic` SDK
- **Company research** — Tavily Search API
- **PDF parsing** — pdfplumber

## Setup

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install streamlit anthropic tavily-python pdfplumber python-dotenv pydantic
```

### 2. Set API keys

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
```

### 3. Run the app

```bash
streamlit run streamlit_app.py
```

## Usage

1. Enter your name and email in the sidebar
2. Enter the company name and paste the full job description
3. Upload your resume as a PDF
4. Click **Generate ✦**

Results appear in four tabs: Cover Letter, Outreach Email, Company Research, and JD Summary. Both documents can be downloaded as `.txt` files and are also saved to `outputs/`.

## Project structure

```
├── streamlit_app.py        # Streamlit frontend
├── main.py                 # FastAPI endpoint (alternative to Streamlit)
├── agent.py                # Orchestrates all steps
├── schemas.py              # AgentInput / AgentOutput models
├── tools/
│   ├── parse_jd.py         # Extracts structured data from job description
│   ├── parse_resume.py     # Matches resume bullets to the role
│   └── search.py           # Tavily company research
├── writers/
│   ├── cover_letter.py     # Cover letter prompt + Claude call
│   └── outreach_email.py   # Cold email prompt + Claude call
└── outputs/                # Generated files saved here
```

## API keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) |
