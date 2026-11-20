**resume-jd-promptX (PromptX)**

A Streamlit app that scores a resume against a job description using the final prompt (V5). Drop your Job Description, Resume and get a match score, the skills the job asks for, the skills your resume shows, what's missing, and three rewritten resume bullets.

**What you get**
- Skills evidenced in the resume
- A 0-100 match score with the math shown (must-have skills 40, experience 40, good-to-have 20)
- A list of missing skills
- Three rewritten bullets grounded in your real experience, with no invented metrics or titles
- Clear error messages for empty or invalid inputs

**Setup**

1. Create and activate a virtual environment:

        python -m venv venv
        source venv/bin/activate

   On Windows, activate with `venv\Scripts\activate` instead.

2. Install dependencies:

        pip install -r requirements.txt

3. Create your environment file:

        cp .env.example .env

   On Windows, use `copy .env.example .env` instead.

4. Open `.env` and paste your key`.

5. Start the app:

        streamlit run app.py

Then open http://localhost:8501.

**Project files**

- `app.py`: landing page, analyzer page, API call, and JSON parsing
- `prompts.py`: the final V5 prompt and the `build_prompt` helper (earlier versions removed)
- `styles.css`: pastel theme, cloud shapes, and transitions
- `.env.example`: template for your API key
- `requirements.txt`: Python dependencies

**How it works**

`build_prompt` fills the resume and job description into the V5 prompt in a single pass, so text inside either document is never substituted a second time. The model replies with a JSON object, which `app.py` parses and displays.

**Output format**

    {
      "jd_skills": [],
      "resume_skills": [],
      "match_score": 0,
      "reason": "",
      "missing_skills": [],
      "rewritten_bullets": []
    }

If an input is missing or isn't a real resume or job posting, the model returns an error object instead of a score.

**Notes**

- Keep your `.env` file private and never commit it.
- Scores come from an AI model and are a guide, not a hiring decision.
