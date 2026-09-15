# SkillPath — AI-Powered Smart Job Matching & Skill Gap Analyzer

A tool that answers the three questions every fresher actually has:

- **Which job suits my current profile?**
- **What skills am I missing for it?**
- **Will my resume even pass an ATS scan?**

Most job portals only search job listings. SkillPath analyzes the *candidate* — resume + target role or job description — and returns a personalized match score, an ATS compatibility check, and a prioritized skill-gap roadmap with where to learn each missing skill.

It covers **54 roles across 13 career fields — IT and non-IT alike**, so it works for a B.Sc Nursing student and a B.Com graduate just as well as for a CSE student.

---

## What's inside

```
smart-job-matcher/
├── frontend/                 # Standalone web app — works with zero setup
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── data.js           # skills + role knowledge base
│       ├── parser.js         # resume text extraction & skill detection
│       ├── matcher.js        # scoring, ATS check, roadmap logic
│       ├── charts.js         # hand-built SVG gauge/radar/bar charts
│       └── app.js            # UI wiring
├── backend/                  # Optional Flask REST API (same logic, in Python)
│   ├── app.py
│   ├── requirements.txt
│   ├── data/skills_database.json   # single source of truth for skills/roles
│   └── utils/
│       ├── skill_data.py
│       ├── parser.py
│       └── matcher.py
├── sample-data/               # Sample resumes (IT and non-IT) to try the tool with
├── build_database.py          # Rebuilds the knowledge base + frontend data file
└── README.md
```

## Two ways to run it

### Option A — Just open it (no install, no server)

Everything in `frontend/` runs entirely in the browser. Resume parsing (PDF via PDF.js, DOCX via Mammoth.js) and all matching logic run client-side — nothing is uploaded anywhere.

```bash
cd frontend
# just open index.html in a browser, or serve it locally:
python3 -m http.server 8000
# then visit http://localhost:8000
```

### Option B — Run the Flask API too (shows full-stack skills)

The backend re-implements the exact same parsing/matching engine in Python and exposes it as a REST API. Useful if you want to demonstrate backend/API design, or plug the engine into another client.

```bash
cd backend
pip install -r requirements.txt
python app.py
# visit http://localhost:5000 — Flask also serves the frontend directly
```

**API reference**

| Endpoint | Method | Description |
|---|---|---|
| `/api/roles` | GET | Full role catalog with required skills |
| `/api/analyze` | POST (multipart) | `resume_text` or `resume_file` + `role_id` or `job_description` → match score, ATS score, roadmap, role ranking |
| `/api/health` | GET | Basic health check |

Example:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "resume_text=@sample-data/sample-resume-fresher.txt;type=text/plain" \
  -F "role_id=frontend-developer"
```

## How the matching actually works

1. **Parse** — extract raw text from the resume (PDF/DOCX/TXT), then detect: skills (against a curated database of 214 skills and their aliases), contact info, resume sections (Education, Skills, Experience, Certifications), and structural signals (bullet points, action verbs, word count).
2. **Match** — every role in the catalog defines its required skills with an importance weight (Must-have / Important / Good-to-have). The candidate's detected skills are compared against the target role's weighted requirements to produce a match percentage. Pasting a real job description instead extracts skill keywords from that text and matches against those.
3. **Score & recommend** — an ATS compatibility score (0–100) is computed from five checks: contact info, section completeness, resume length, bullet/action-verb usage, and keyword alignment. Missing skills are ranked by importance into a roadmap, each with a specific free learning resource and action.
4. **Rank** — every role in the catalog is scored against the candidate's actual detected skills, surfacing roles that might be a better fit than the one originally picked.

This is a transparent, rules-based matching engine (weighted skill overlap + keyword extraction) — not a black box. That's a deliberate choice: it's explainable, fast, needs no API key, and every score can be traced back to a specific reason.

## Role coverage

| Field | Roles |
|---|---|
| Information Technology | Frontend, Backend, Full Stack, Android, QA, DevOps, Cloud, DBA, Cybersecurity, Technical Support |
| Data & AI | Data Analyst, Data Scientist, ML Engineer |
| Core Engineering | Mechanical Design, Production, Quality (QA/QC), Civil, Site Engineer, Electrical, Electronics/Embedded, Automobile |
| Finance & Accounting | Accountant, Financial Analyst, Audit Associate, Tax Associate, Banking Officer |
| Healthcare | Staff Nurse, Pharmacist, Medical Lab Technician, Physiotherapist |
| Business & Operations | Business Analyst, Operations, Supply Chain/Logistics, Project Coordinator, Data Entry |
| Marketing & Sales | Sales, Business Development, Customer Support, Retail Store Manager |
| Design & Creative | UI/UX, Graphic Designer, Video Editor, Content Writer, Journalist |
| Human Resources | HR Recruiter, HR Generalist |
| Education | School Teacher, Academic Content Developer |
| Hospitality & Tourism | Hotel Front Office, Chef, Event Manager |
| Legal | Legal Associate |
| Agriculture | Agriculture Officer |

## Extending it

- **Add a skill or role**: open `build_database.py`, add your entry using the `skill()`, `resource()`, and `role()` helpers, then run:
  ```bash
  python3 build_database.py
  ```
  It validates that every role references real skills and that every skill has a learning resource, then writes both `backend/data/skills_database.json` and `frontend/js/data.js` so the two engines never drift apart.
- **Swap in a real LLM**: `matcher.js` / `matcher.py` are isolated modules — the weighted-overlap scoring could be replaced with an embedding-similarity or LLM-based scorer without touching the UI.
- **Add resume storage / accounts**: the Flask backend is the natural place to add a database and auth if this grows beyond a single-session tool.

## Tech stack

Frontend: HTML5, CSS3 (custom design system, no UI framework), vanilla JavaScript, PDF.js, Mammoth.js, hand-built SVG data visualizations.
Backend: Python, Flask, pypdf, python-docx.

---

Built as a portfolio project demonstrating resume parsing, rules-based matching/recommendation logic, ATS-awareness, and a from-scratch interactive UI.
