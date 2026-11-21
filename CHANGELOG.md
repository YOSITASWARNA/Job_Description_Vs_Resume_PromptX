# Changelog

## v3 (committed Oct 25, 2026)
Working Streamlit prototype using Prompt v3, from the earlier repository.
- Rubric and JSON output format with the math shown in "reason".
- Edge-case rule for empty or missing input.
- Rewritten bullets are limited to facts stated in the resume.

## v4 (not committed)
Prompt used during development but never committed to git.
- Scoring rubric: 40 must-have skills, 40 experience, 20 good-to-have, with the math shown in "reason".
- Empty-input check returns {"error": "Missing input"}.
- Output is JSON only, with six keys.
- Input markers: ###RESUME### and ###JOB DESCRIPTION###.

## v5 (committed Nov 20, 2026)
Final prompt, committed in the PromptX repository.
- Semantic validation: if the resume or job description is not real, returns {"error": "Invalid input provided. Please paste a valid resume and job description."} without scoring.
- Edge-case rule also skips scoring and validation when input is empty.
- Bullet rewrites may not add unstated metrics, job titles, stakeholders, or outcomes.
- Input markers changed to ### RESUME ### and ### JOB DESCRIPTION ### (formatting only).