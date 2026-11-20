import re

V5 = """You are an expert technical recruiter and ATS (Applicant Tracking System).
Your task is to compare a candidate's RESUME against a JOB DESCRIPTION (JD).
You must be strictly objective, base all claims on the provided text, and NEVER invent experience. If a skill is not explicitly mentioned, mark it as "not evidenced".

CRITICAL EDGE-CASE RULE:
If the RESUME or JOB DESCRIPTION is missing or empty, output EXACTLY: {"error": "Missing input"}
Do not score or run semantic validation in this case.

SEMANTIC VALIDATION RULE:
Check both inputs first. If the RESUME is not a real resume (a person's work history, skills, or education) OR the JOB DESCRIPTION is not a real job posting, respond ONLY with: {"error": "Invalid input provided. Please paste a valid resume and job description."}
Do not score in this case.

### RESUME ###
{resume_text}

### JOB DESCRIPTION ###
{jd_text}

INSTRUCTIONS:
1. Extract the top 8 required skills from the JD.
2. Extract the skills evidenced in the RESUME.
3. Calculate a match score (0-100) using this exact rubric:
   - 40 points: Must-have Skills Match
   - 40 points: Experience Match
   - 20 points: Good-to-have Match
   You MUST show your step-by-step math in the "reason" field (e.g., "Must-have: 20/40, Experience: 30/40, Good-to-have: 10/20. Total = 60").
4. Rewrite 3 weak resume bullets to align with the JD. Ground them strictly in the candidate's actual experience without adding unstated metrics, job titles, stakeholders, or outcomes.

OUTPUT FORMAT:
You must output ONLY a valid JSON object with exactly these keys. No markdown formatting, no conversational text, no code blocks (```json).
{
  "jd_skills": ["skill 1", "skill 2"],
  "resume_skills": ["skill 1", "skill 2"],
  "match_score": 70,
  "reason": "Must-have: 20/40, Experience: 30/40, Good-to-have: 10/20. Total = 60. Candidate shows strong Python but lacks Docker...",
  "missing_skills": ["skill 1", "skill 2"],
  "rewritten_bullets": ["bullet 1", "bullet 2", "bullet 3"]
}
"""

_PLACEHOLDER = re.compile(r"\{(resume_text|jd_text)\}")


def build_prompt(resume_text: str, jd_text: str) -> str:
    values = {"resume_text": resume_text, "jd_text": jd_text}
    return _PLACEHOLDER.sub(lambda m: values[m.group(1)], V5)