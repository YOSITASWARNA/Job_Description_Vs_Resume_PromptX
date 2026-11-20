import html
import json
import logging
import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from prompts import build_prompt

BASE = Path(__file__).parent

FIX_CSS = """
html body .stApp [data-testid="stTextArea"] div,
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] div,
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"],
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"] div,
html body .stApp [data-testid="stTextInput"] [data-baseweb="base-input"] {
  background-color: #ffffff !important; color: #0f1b3d !important;
}
html body .stApp textarea, html body .stApp input {
  background-color: #ffffff !important; color: #0f1b3d !important;
  -webkit-text-fill-color: #0f1b3d !important; caret-color: #0f1b3d !important;
}
html body .stApp textarea { border: 2px solid #d3effb !important; border-radius: 26px !important; padding: 1rem 1.2rem !important; box-shadow: none !important; }
html body .stApp textarea:focus { border-color: #19a7a3 !important; box-shadow: 0 0 0 4px rgba(25,167,163,.15) !important; }
html body .stApp textarea::placeholder, html body .stApp input::placeholder { color: #7f8db0 !important; -webkit-text-fill-color: #7f8db0 !important; opacity: 1 !important; }
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"] { border: 2px solid #d3effb !important; border-radius: 20px !important; }
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"] > div, html body .stApp [data-testid="stTextInput"] input { border: 0 !important; }
html body .stApp [data-testid="stTextInput"] button { background-color: transparent !important; opacity: 1 !important; }
html body .stApp [data-testid="stTextInput"] button svg, html body .stApp [data-testid="stTextInput"] button svg * {
  color: #0f1b3d !important; fill: #0f1b3d !important; opacity: 1 !important;
}
html body .stApp [data-baseweb="select"] *, html body .stApp [data-baseweb="select"] svg { color: #0f1b3d !important; fill: #0f1b3d !important; }
html body [data-baseweb="popover"] *, html body [data-baseweb="menu"] * { background-color: #ffffff !important; color: #0f1b3d !important; }
html body [data-baseweb="popover"] li:hover, html body [data-baseweb="menu"] li:hover { background-color: #eaf7ff !important; }
html body .stApp [data-testid="stFileUploaderFile"] { background-color: #eef8ff !important; border-radius: 16px !important; }
html body .stApp [data-testid="stFileUploaderFile"] * { background-color: transparent !important; color: #0f1b3d !important; }
html body .stApp [data-testid="stFileUploaderDropzone"] { background-color: #ffffff !important; }
html body .stApp [data-testid="stFileUploaderDropzone"] * { color: #5b6b94 !important; }
html body .stApp [data-testid="stFileUploaderDropzone"] button { background-color: #ffffff !important; }
html body .stApp [data-testid="stFileUploaderDropzone"] button * { color: #0f1b3d !important; }
html body .stApp [data-testid="stHeading"], html body .stApp [data-testid="stHeading"] * { color: #0f1b3d !important; }
html body .stApp .st-key-jd_cloud [data-testid="stMarkdownContainer"] *,
html body .stApp .st-key-resume_cloud [data-testid="stMarkdownContainer"] * { color: #0f1b3d !important; }
html body .stApp [data-testid="stWidgetLabel"] *, html body .stApp [data-testid="stSpinner"] * { color: #0f1b3d !important; }
html body .stApp [data-testid="stWidgetLabel"], html body .stApp [data-testid="stWidgetLabel"] * { background-color: transparent !important; }
html body .stApp [data-testid="stCaptionContainer"] * { color: #5b6b94 !important; }
html body .stApp [data-testid="stTextArea"] div { border: 0 !important; border-radius: 26px !important; box-shadow: none !important; }
.spark line { animation: none !important; }
html body .stApp [data-testid="stMainBlockContainer"] { padding-top: 4.2rem !important; }
.logo { position: fixed; top: 10px; left: 14px; z-index: 99999; margin: 0; padding: 0; background: none !important; border: 0; box-shadow: none; }
.logo img { height: 44px; width: auto; display: block; filter: drop-shadow(0 0 3px rgba(255, 255, 255, .7)); }
html body .stApp [data-testid="stHeader"], html body .stApp [data-testid="stDecoration"], html body .stApp [data-testid="stToolbar"] {
  display: none !important; height: 0 !important; border: 0 !important; box-shadow: none !important; background: transparent !important;
}
html body .stApp [data-testid="stTextInput"] > div > div,
html body .stApp [data-testid="stSelectbox"] > div > div,
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"],
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div {
  background-color: #ffffff !important; border: 2px solid #d3effb !important; border-radius: 20px !important;
  box-shadow: none !important; overflow: hidden;
}
html body .stApp [data-testid="stTextInput"] > div > div *,
html body .stApp [data-testid="stSelectbox"] > div > div *,
html body .stApp [data-testid="stTextInput"] [data-baseweb="input"] *,
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div * {
  background: #ffffff !important; background-color: #ffffff !important; border: 0 !important;
  box-shadow: none !important; outline: 0 !important; color: #0f1b3d !important;
}
html body .stApp [data-testid="stTextInput"] > div, html body .stApp [data-testid="stSelectbox"] > div { background-color: transparent !important; }
html body .stApp [data-testid="stTextInput"] > div > div:focus-within,
html body .stApp [data-testid="stSelectbox"] > div > div:focus-within { border-color: #19a7a3 !important; }
html body [data-testid="stSelectboxVirtualDropdown"], html body [data-testid="stSelectboxVirtualDropdown"] *,
html body [role="listbox"], html body [role="listbox"] *, html body [role="option"] {
  background-color: #ffffff !important; color: #0f1b3d !important;
}
html body [role="option"]:hover, html body [role="option"][aria-selected="true"] { background-color: #eaf7ff !important; }
html body .stApp .stage h1 { font-size: clamp(1.3rem, 4.1cqw, 4.4rem) !important; }
.steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; align-items: stretch; }
@media (max-width: 760px) {
  .steps-grid { grid-template-columns: 1fr; gap: 1rem; }
  .logo { position: absolute; }
  .logo img { height: 36px; }
}
"""


KEY_SHAPES = re.compile(r"AIza[0-9A-Za-z_\-]{20,}|sk-ant-[0-9A-Za-z_\-]{10,}|sk-[0-9A-Za-z_\-]{20,}")


class _KeyScrubFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        clean = KEY_SHAPES.sub("[hidden]", msg)
        if clean != msg:
            record.msg = clean
            record.args = ()
        return True


def install_key_scrubber() -> None:
    scrub = _KeyScrubFilter()
    for name in (None, "streamlit", "httpx", "httpcore", "google", "openai", "anthropic"):
        logger = logging.getLogger(name)
        if not any(isinstance(f, _KeyScrubFilter) for f in logger.filters):
            logger.addFilter(scrub)
        for handler in logger.handlers:
            if not any(isinstance(f, _KeyScrubFilter) for f in handler.filters):
                handler.addFilter(scrub)


install_key_scrubber()


def redact(text, *secrets: str) -> str:
    text = str(text)
    for secret in secrets:
        if secret:
            text = text.replace(secret, "[hidden]")
    return KEY_SHAPES.sub("[hidden]", text)


def key_format_ok(key: str) -> bool:
    return 20 <= len(key) <= 200 and not re.search(r"\s", key)


RESUME_SECTIONS = [
    "experience", "work experience", "work history", "employment", "education",
    "skills", "technical skills", "projects", "certifications", "certificates",
    "summary", "objective", "profile", "achievements", "awards", "publications",
    "internship", "internships", "languages", "interests", "references",
]
JD_KEYWORDS = [
    "responsibilities", "requirements", "qualifications", "about the role",
    "we are looking", "we are hiring", "you will", "what you will",
    "must have", "nice to have", "preferred qualifications", "benefits",
    "salary", "years of experience", "job description", "apply now",
]
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
UPLOAD_HINT = "Upload a correct resume file (PDF, DOCX, or TXT)."
BOTH_RESUME_INPUTS = "You added both a resume file and pasted text. Use only one: remove the file or clear the text box."


def looks_like_real_text(text: str, min_words: int = 40) -> bool:
    text = text.strip()
    if len(text) < 150:
        return False
    words = re.findall(r"[A-Za-z][A-Za-z+#.]*", text)
    if len(words) < min_words:
        return False
    if len({w.lower() for w in words}) / len(words) < 0.25:
        return False
    if re.search(r"(.)\1{7,}", text):
        return False
    if sum(c.isalpha() for c in text) / max(len(text), 1) < 0.5:
        return False
    return True


def is_resume(text: str) -> bool:
    low = text.lower()
    section_hits = sum(1 for s in RESUME_SECTIONS if re.search(rf"\b{re.escape(s)}\b", low))
    has_contact = bool(EMAIL_RE.search(text) or PHONE_RE.search(text))
    jd_hits = sum(1 for k in JD_KEYWORDS if k in low)
    if jd_hits >= 2 and not has_contact:
        return False
    return section_hits >= 2 or (section_hits >= 1 and has_contact)


def is_job_description(text: str) -> bool:
    low = text.lower()
    return sum(1 for k in JD_KEYWORDS if k in low) >= 2


def validate_jd(jd: str) -> str | None:
    if not jd.strip():
        return "Paste the job description."
    if not looks_like_real_text(jd):
        return "The job description doesn't look like readable text. Paste the full job posting."
    if not is_job_description(jd):
        return "The job description doesn't look like a job posting. Check the text in that box."
    return None


def validate_resume(text: str, source: str) -> str | None:
    if not looks_like_real_text(text):
        return f"The resume from {source} doesn't contain readable resume text. {UPLOAD_HINT}"
    if not is_resume(text):
        return (f"The resume from {source} doesn't look like a resume (no experience, education, "
                f"or skills sections found). {UPLOAD_HINT}")
    return None


@st.cache_data
def load_logo_b64(path: str, mtime: float) -> str:
    import base64
    import io

    import numpy as np
    from PIL import Image

    arr = np.asarray(Image.open(path).convert("RGBA")).astype(float)
    rgb, alpha = arr[..., :3], arr[..., 3]
    if alpha.min() > 250:
        m = rgb.min(axis=2)
        a = np.clip((248 - m) / 248, 0, 1)
        a = np.where(a < 0.03, 0, a)
        rgb = np.clip((rgb - (1 - a)[..., None] * 255) / np.maximum(a, 1e-3)[..., None], 0, 255)
        arr = np.dstack([rgb, a * 255])
    im = Image.fromarray(arr.astype("uint8"), "RGBA")
    if im.getbbox():
        im = im.crop(im.getbbox())
    im.thumbnail((520, 200))
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def logo_html() -> str:
    p = BASE / "logo.png"
    if p.exists():
        return f'<div class="logo"><img src="data:image/png;base64,{load_logo_b64(str(p), p.stat().st_mtime)}" alt="PromptX"></div>'
    return '<div class="logo"><b style="font-size:1.6rem;color:#0f1b3d">PromptX</b></div>'


DEFAULT_GEMINI_KEY = ""

for _name in (".env", ".env.txt", "_.env", "env"):
    _p = BASE / _name
    if _p.exists():
        load_dotenv(_p, override=True, encoding="utf-8-sig")

st.set_page_config(
    page_title="PromptX · Job Description ⇄ Resume",
    page_icon="🗒️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(f"<style>{(BASE / 'styles.css').read_text(encoding='utf-8')}{FIX_CSS}</style>",
            unsafe_allow_html=True)

PROVIDERS = {
    "Google (Gemini)": {
        "short": "Gemini", "env": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
        "model_env": "GEMINI_MODEL", "model": "gemini-2.5-flash", "default": DEFAULT_GEMINI_KEY,
    },
    "Anthropic (Claude)": {
        "short": "Claude", "env": ["ANTHROPIC_API_KEY"],
        "model_env": "ANTHROPIC_MODEL", "model": "claude-sonnet-4-6", "default": "",
    },
    "OpenAI (GPT)": {
        "short": "OpenAI", "env": ["OPENAI_API_KEY"],
        "model_env": "OPENAI_MODEL", "model": "gpt-4o-mini", "default": "",
    },
}


def get_key(provider: str, typed: str) -> str:
    cfg = PROVIDERS[provider]
    key = typed.strip()
    if not key:
        for name in cfg["env"]:
            key = os.getenv(name, "").strip()
            if key:
                break
    if not key:
        key = cfg["default"].strip()
    return key.strip('"').strip("'")


def call_llm(provider: str, prompt: str, key: str) -> str:
    cfg = PROVIDERS[provider]
    model = os.getenv(cfg["model_env"], cfg["model"])

    if provider.startswith("Anthropic"):
        from anthropic import Anthropic

        msg = Anthropic(api_key=key).messages.create(
            model=model,
            max_tokens=2000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")

    if provider.startswith("OpenAI"):
        from openai import OpenAI

        r = OpenAI(api_key=key).chat.completions.create(
            model=model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        return r.choices[0].message.content or ""

    if provider.startswith("Google"):
        from google import genai

        client = genai.Client(api_key=key)
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={"temperature": 0},
            )
            return response.text or ""
        finally:
            client.close()

    raise ValueError(f"Unsupported provider: {provider}")


def read_upload(f) -> str:
    f.seek(0)
    name = f.name.lower()
    if name.endswith(".pdf"):
        from pypdf import PdfReader

        text = "\n".join((p.extract_text() or "") for p in PdfReader(f).pages)
    elif name.endswith(".docx"):
        import docx

        d = docx.Document(f)
        parts = [p.text for p in d.paragraphs]
        for table in d.tables:
            for row in table.rows:
                for cell in row.cells:
                    parts.append(cell.text)
        text = "\n".join(parts)
    else:
        text = f.read().decode("utf-8", errors="ignore")
    return re.sub(r"[ \t]+", " ", text).strip()


def parse_json(raw: str) -> dict:
    if raw is None or not str(raw).strip():
        return {"error": "The AI provider returned an empty response. Try again."}

    raw = re.sub(r"^```(?:json)?|```$", "", str(raw).strip(), flags=re.MULTILINE).strip()

    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        return {"error": "Could not read the model's answer. Try again."}

    try:
        return json.loads(raw[start:end + 1])
    except json.JSONDecodeError:
        return {"error": "The model returned invalid JSON. Try again."}


def analyze(resume: str, jd: str, provider: str, key: str) -> dict:
    return parse_json(call_llm(provider, build_prompt(resume, jd), key))


QUOTA_MARKERS = (
    "429", "resource_exhausted", "quota", "rate limit", "rate_limit",
    "insufficient_quota", "too many requests",
)


def is_quota_error(e: Exception) -> bool:
    text = f"{type(e).__name__} {e}".lower()
    return any(marker in text for marker in QUOTA_MARKERS)


def quota_message(short: str) -> str:
    return (f"The {short} API limit has been reached for now. "
            f"Paste your own {short} API key in the API key box above, then click Analyze Match again.")


def test_key(provider: str, key: str) -> str | None:
    try:
        if provider.startswith("Google"):
            from google import genai

            client = genai.Client(api_key=key)
            try:
                next(iter(client.models.list()), None)
            finally:
                client.close()
        elif provider.startswith("Anthropic"):
            from anthropic import Anthropic

            Anthropic(api_key=key).models.list(limit=1)
        else:
            from openai import OpenAI

            OpenAI(api_key=key).models.list()
        return None
    except Exception as e:
        if is_quota_error(e):
            return None
        return "That API key was not accepted. Check it and try again."


def stash_typed_key() -> None:
    st.session_state["_run_key"] = st.session_state.get("typed_key", "")
    st.session_state["typed_key"] = ""


def esc(x) -> str:
    return html.escape(str(x))


def chips(items, kind="") -> str:
    return "".join(f'<span class="cloud chip {kind}">{esc(i)}</span>' for i in items)


def ring(score) -> str:
    try:
        score = max(0, min(100, int(score)))
    except (TypeError, ValueError):
        score = 0
    tone = "hi" if score >= 70 else "mid" if score >= 45 else "lo"
    return f'<div class="ring {tone}" style="--p:{score}"><span>{score}</span></div>'


def clipboard_rows() -> str:
    out = ""
    for y in (530, 590, 650, 710):
        out += (
            f'<path d="M150 {y} l16 16 l28 -34" fill="none" stroke="#2ed3b7" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<rect x="215" y="{y - 18}" width="115" height="26" rx="13" fill="#d3e7fa"/>'
        )
    return out


def line(x1, y1, x2, y2, color, w=6, op=1) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round"/>'
    )


HERO_SVG = (
    '<svg class="hero-svg" viewBox="0 0 1672 941" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    '<g fill="none" stroke="#86c5f0" stroke-width="3" class="dash">'
    '<path d="M365 505 Q600 462 795 478"/><path d="M878 478 Q1100 468 1312 510"/>'
    '<path d="M385 592 Q600 562 795 578"/><path d="M878 578 Q1100 564 1300 596"/>'
    '<path d="M388 648 Q600 692 795 686"/><path d="M878 686 Q1100 692 1286 650"/>'
    "</g>"
    '<g class="f1"><g transform="rotate(-8 250 600)">'
    '<rect x="112" y="445" width="270" height="310" rx="30" fill="#eef8ff" stroke="#9fd0f7" stroke-width="3"/>'
    '<rect x="195" y="425" width="88" height="42" rx="18" fill="#b9dcfb"/>'
    + clipboard_rows()
    + "</g></g>"
    '<g class="f2"><g transform="rotate(8 1420 580)">'
    '<rect x="1300" y="430" width="255" height="300" rx="30" fill="#f3faff" stroke="#a8d3f7" stroke-width="3"/>'
    '<circle cx="1380" cy="500" r="34" fill="#a9d4f8"/>'
    '<rect x="1438" y="484" width="90" height="22" rx="11" fill="#cfe3f8"/>'
    '<rect x="1432" y="518" width="80" height="20" rx="10" fill="#cfe3f8"/>'
    '<rect x="1335" y="565" width="170" height="24" rx="12" fill="#d3e7fa"/>'
    '<rect x="1335" y="605" width="140" height="24" rx="12" fill="#d3e7fa"/>'
    '<rect x="1335" y="645" width="110" height="24" rx="12" fill="#d3e7fa"/>'
    "</g>"
    '<circle cx="1520" cy="700" r="60" fill="#cfe9ff" fill-opacity="0.55" stroke="#4f9fe3" stroke-width="14"/>'
    '<path d="M1490 672 Q1503 656 1522 654" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" opacity="0.8"/>'
    + line(1565, 745, 1618, 797, "#3b86d1", 22)
    + "</g>"
    '<g class="f3"><g transform="rotate(8 1470 165)">'
    '<rect x="1395" y="82" width="160" height="150" rx="8" fill="#ffdbe8" stroke="#ff8db6" stroke-width="3"/>'
    '<polygon points="1440,104 1446,118 1461,119 1450,129 1453,144 1440,136 1427,144 1430,129 1419,119 1434,118" '
    'fill="none" stroke="#2ed3b7" stroke-width="3" stroke-linejoin="round"/>'
    '<rect x="1422" y="172" width="100" height="14" rx="7" fill="#ff9cc0"/>'
    '<rect x="1422" y="196" width="70" height="14" rx="7" fill="#ff9cc0"/>'
    '<path d="M1555 232 L1510 232 L1555 192 Z" fill="#ffb5d0"/>'
    + line(1560, 65, 1566, 43, "#3ddbc7", 7, 0.95)
    + line(1569, 70, 1586, 56, "#3ddbc7", 7, 0.95)
    + line(1573, 80, 1595, 78, "#3ddbc7", 7, 0.95)
    + "</g></g>"
    '<g class="dot d1"><circle cx="836" cy="478" r="32" fill="#effcf8" stroke="#2fd4b0" stroke-width="4"/>'
    '<path d="M819 479 l13 13 l22 -26" fill="none" stroke="#2fd4b0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    '<g class="dot d2"><circle cx="836" cy="578" r="32" fill="#effcf8" stroke="#2fd4b0" stroke-width="4"/>'
    '<path d="M819 579 l13 13 l22 -26" fill="none" stroke="#2fd4b0" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g>'
    '<g class="dot d3"><circle cx="836" cy="686" r="32" fill="#fff2f4" stroke="#ff4d63" stroke-width="4"/>'
    '<path d="M821 671 L851 701 M851 671 L821 701" fill="none" stroke="#ff4d63" stroke-width="6" stroke-linecap="round"/></g>'
    "</svg>"
)

HERO = (
    '<div class="stage">' + HERO_SVG +
    '<div class="hero-copy"><h1>Job Description <span class="swap">⇄</span> Resume</h1>'
    '<p class="sub">Your Potential. The Right Role. The Perfect Match.</p>'
    '</div></div>'
)

TERMS = chips(["ATS Match Score", "JD Keywords", "Skill Gap", "Missing Skills", "Bullet Rewrite"])


def show_alerts(messages) -> None:
    for msg in messages:
        st.markdown(f'<div class="cloud alert">{esc(msg)}</div>', unsafe_allow_html=True)


def show_result(res) -> None:
    if not res:
        return
    if "errors" in res:
        show_alerts(res["errors"])
        return
    if "error" in res:
        msg = res["error"]
        if msg.lower().startswith("missing input"):
            msg = "Missing input. Please provide both a resume and a job description."
        show_alerts([msg])
        return

    if st.session_state.get("source_note"):
        st.caption(st.session_state.source_note)

    jd_skills = res.get("jd_skills", [])
    missing = [str(m).lower() for m in res.get("missing_skills", [])]

    def is_missing(skill: str) -> bool:
        s = str(skill).lower()
        return any(s in m or m in s for m in missing)

    st.markdown(
        '<div class="card score">' + ring(res.get("match_score", 0))
        + '<div><h3>ATS match score</h3>'
        f'<p class="reason">{esc(res.get("reason", ""))}</p></div></div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2, gap="large")
    with c1:
        tags = "".join(
            f'<span class="cloud chip {"miss" if is_missing(s) else "hit"}">'
            f'{"✕" if is_missing(s) else "✓"} {esc(s)}</span>' for s in jd_skills
        )
        st.markdown(f'<div class="card"><h3>Top JD skills</h3><div class="chips">{tags}</div></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown(
            f'<div class="card"><h3>Skills on your resume</h3><div class="chips">'
            f'{chips(res.get("resume_skills", []), "hit")}</div></div>',
            unsafe_allow_html=True,
        )
    gap = chips(res.get("missing_skills", []), "miss") or "<p>No gaps found.</p>"
    st.markdown(f'<div class="card"><h3>Skill gap</h3><div class="chips">{gap}</div></div>',
                unsafe_allow_html=True)
    bullets = "".join(f"<li>{esc(b)}</li>" for b in res.get("rewritten_bullets", []))
    st.markdown(f'<div class="card"><h3>Rewritten bullets</h3><ol class="bullets">{bullets}</ol></div>',
                unsafe_allow_html=True)


if "result" not in st.session_state:
    st.session_state.result = None
if "source_note" not in st.session_state:
    st.session_state.source_note = ""

st.markdown(logo_html(), unsafe_allow_html=True)
st.markdown(HERO, unsafe_allow_html=True)
st.markdown(f'<div class="term-row">{TERMS}</div>', unsafe_allow_html=True)

st.markdown("## How it works")
steps = [
    ("1", "Add the job description",
     "Paste the full posting. Requirements and responsibilities give the best results."),
    ("2", "Add your resume",
     "Upload a PDF, DOCX, or TXT file or paste the resume text. Use one of these, not both. "
     "Scanned PDFs with no text layer can't be read."),
    ("3", "Get your match",
     "See a score out of 100, the skills you're missing, and three rewritten bullets."),
]
cards = "".join(
    f'<div class="card" style="margin:0;height:100%;box-sizing:border-box">'
    f'<h3>{num}. {esc(title)}</h3><p>{esc(text)}</p></div>'
    for num, title, text in steps
)
st.markdown(
    '<div class="steps-grid">' + cards + "</div>",
    unsafe_allow_html=True,
)
st.markdown("<div style='height:3.5rem'></div>", unsafe_allow_html=True)
st.markdown(
    '<p class="section-sub">Drop your Job Description and resume.</p>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")
with left:
    with st.container(key="jd_cloud"):
        st.markdown("#### Job description")
        jd_text = st.text_area("Job description", height=300, key="jd", label_visibility="collapsed",
                               placeholder="Paste the job description here…")
with right:
    with st.container(key="resume_cloud"):
        st.markdown("#### Resume")
        up = st.file_uploader("Upload resume", type=["pdf", "docx", "txt"], label_visibility="collapsed")
        resume_pasted = st.text_area("Resume text", height=180, key="resume", label_visibility="collapsed",
                                     placeholder="…or paste your resume text here")
        st.caption("Use either a file or pasted text, not both.")

pc1, pc2 = st.columns(2, gap="large")
with pc1:
    provider = st.selectbox("AI provider", list(PROVIDERS.keys()), index=0)
cfg = PROVIDERS[provider]
has_saved = bool(get_key(provider, ""))
with pc2:
    st.text_input(
        f"{cfg['short']} API key" + (" (optional)" if has_saved else ""),
        type="password",
        key="typed_key",
        placeholder="Leave blank to use the saved key" if has_saved else f"Paste your {cfg['short']} API key",
    )
    st.markdown(
        '<p class="section-sub" style="text-align:left;margin-top:0.4rem">'
        'Used only for this request. It is not saved, shown, or logged, '
        'and the box clears after each run.</p>',
        unsafe_allow_html=True,
    )

_, mid, _ = st.columns([2, 1.3, 2])
with mid:
    run = st.button("Analyze Match", key="analyze", use_container_width=True, on_click=stash_typed_key)

if run:
    run_key = st.session_state.pop("_run_key", "").strip().strip('"').strip("'")
    key = ""
    result = None
    source_note = ""
    try:
        typed_clean = bool(run_key)
        key = get_key(provider, run_key)

        errors = []
        jd_error = validate_jd(jd_text)
        if jd_error:
            errors.append(jd_error)

        resume_text, resume_source = "", None
        if up is not None and resume_pasted.strip():
            errors.append(BOTH_RESUME_INPUTS)
        elif up is not None:
            resume_source = up.name
            try:
                resume_text = read_upload(up)
            except Exception:
                errors.append(f"{up.name} could not be read. {UPLOAD_HINT}")
                resume_source = None
        elif resume_pasted.strip():
            resume_text, resume_source = resume_pasted, "pasted text"
        else:
            errors.append(f"Upload your resume or paste its text, not both. {UPLOAD_HINT}")

        if resume_source is not None:
            resume_error = validate_resume(resume_text, resume_source)
            if resume_error:
                errors.append(resume_error)
            else:
                source_note = f"Analysed resume from: {resume_source} ({len(resume_text.split())} words)"

        if errors:
            result = {"errors": errors}
        elif not key:
            result = {
                "error": f"No {cfg['short']} API key found. Paste it in the API key box above"
                + (f", or add {cfg['env'][0]} to your .env file next to app.py." if provider.startswith("Google") else ".")
            }
        elif typed_clean and not key_format_ok(run_key):
            result = {"error": "That doesn't look like an API key. Check it and try again."}
        else:
            with st.spinner("Matching JD keywords against your resume…"):
                key_problem = test_key(provider, key) if typed_clean else None
                if key_problem:
                    result = {"error": key_problem}
                else:
                    result = analyze(resume_text, jd_text, provider, key)
    except Exception as e:
        if is_quota_error(e):
            result = {"error": quota_message(cfg["short"])}
        else:
            result = {"error": redact(f"Request failed: {e}", key, run_key)}

    st.session_state.result = result
    st.session_state.source_note = source_note

show_result(st.session_state.result)