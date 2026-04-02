import streamlit as st
import pdfplumber
import io
import os
from agent import run
from schemas import AgentInput

st.set_page_config(
    page_title="Cover Letter & Outreach Agent",
    page_icon="✉️",
    layout="wide",
)

st.title("Cover Letter & Outreach Email Agent")
st.caption("Paste a job description, upload your resume, and get a tailored cover letter and cold email in seconds.")

# ── Sidebar: inputs ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Your Details")
    user_name = st.text_input("Full name", placeholder="Jane Smith")
    user_email = st.text_input("Email", placeholder="jane@example.com")

    st.header("Role Details")
    company_name = st.text_input("Company name", placeholder="Acme Corp")
    job_description = st.text_area(
        "Job description",
        placeholder="Paste the full JD here…",
        height=220,
    )

    st.header("Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    run_button = st.button("Generate ✦", type="primary", use_container_width=True)

# ── Helper ───────────────────────────────────────────────────────────────────
def extract_pdf_text(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

# ── Main panel ───────────────────────────────────────────────────────────────
if run_button:
    missing = []
    if not user_name:
        missing.append("Full name")
    if not user_email:
        missing.append("Email")
    if not company_name:
        missing.append("Company name")
    if not job_description:
        missing.append("Job description")
    if not uploaded_file:
        missing.append("Resume PDF")

    if missing:
        st.error(f"Please fill in: {', '.join(missing)}")
        st.stop()

    resume_text = extract_pdf_text(uploaded_file.read())

    agent_input = AgentInput(
        company_name=company_name,
        job_description=job_description,
        resume_text=resume_text,
        user_name=user_name,
        user_email=user_email,
    )

    # Progress display
    progress_placeholder = st.empty()
    step_labels = [
        "Parsing job description",
        f"Researching {company_name}",
        "Matching resume to role",
        "Writing cover letter",
        "Writing outreach email",
    ]

    with progress_placeholder.container():
        st.subheader("Working…")
        bars = []
        for label in step_labels:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"◦ {label}")
            bars.append(col2.empty())

    with st.spinner(""):
        result = run(agent_input)

    # Update progress to done
    progress_placeholder.empty()

    # Save outputs
    os.makedirs("outputs", exist_ok=True)
    slug = company_name.lower().replace(" ", "_")
    with open(f"outputs/{slug}_cover_letter.txt", "w") as f:
        f.write(result.cover_letter)
    with open(f"outputs/{slug}_outreach_email.txt", "w") as f:
        f.write(result.outreach_email)

    st.success(f"Done! Files saved to `outputs/{slug}_*.txt`")

    # ── Tabs: main outputs ───────────────────────────────────────────────────
    tab_cl, tab_email, tab_research, tab_jd = st.tabs([
        "Cover Letter", "Outreach Email", "Company Research", "JD Summary"
    ])

    with tab_cl:
        st.subheader("Cover Letter")
        st.text_area(
            label="cover_letter",
            value=result.cover_letter,
            height=420,
            label_visibility="collapsed",
        )
        st.download_button(
            "Download .txt",
            data=result.cover_letter,
            file_name=f"{slug}_cover_letter.txt",
            mime="text/plain",
        )

    with tab_email:
        st.subheader("Outreach Email")
        st.text_area(
            label="outreach_email",
            value=result.outreach_email,
            height=300,
            label_visibility="collapsed",
        )
        st.download_button(
            "Download .txt",
            data=result.outreach_email,
            file_name=f"{slug}_outreach_email.txt",
            mime="text/plain",
        )

    with tab_research:
        st.subheader("Company Research")
        st.write(result.company_research)

    with tab_jd:
        st.subheader("Parsed JD Summary")
        col_skills, col_summary = st.columns(2)
        with col_skills:
            st.write("**Required Skills**")
            for skill in result.jd_summary.get("required_skills", []):
                st.markdown(f"- {skill}")
        with col_summary:
            st.write("**Role Summary**")
            st.write(result.jd_summary.get("role_summary", "—"))
            if result.jd_summary.get("role_title"):
                st.caption(f"Title: {result.jd_summary['role_title']}")

        st.divider()
        st.write("**Resume Highlights Used**")
        for highlight in result.resume_highlights:
            st.markdown(f"- {highlight}")

    # ── Agent trace (collapsed) ──────────────────────────────────────────────
    with st.expander("Agent steps"):
        for step in result.steps_taken:
            status_icon = "✓" if step["status"] == "done" else "…"
            st.markdown(f"**{status_icon} {step['step']}**")
            if step.get("result"):
                st.json(step["result"], expanded=False)

else:
    # Empty state
    st.info("Fill in your details in the sidebar and click **Generate ✦** to get started.")
