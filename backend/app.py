"""
SkillPath API — optional Flask backend.

The website in /frontend works fully standalone (all matching logic
runs client-side in JavaScript). This API exists to show the same
analysis engine implemented server-side in Python, and to support
programmatic / mobile clients that would rather call a REST API
than ship the matching logic themselves.

Run:
    pip install -r requirements.txt
    python app.py
Then visit http://localhost:5000
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from utils.skill_data import SKILL_DB, ROLES
from utils.parser import extract_text, analyze_resume_text
from utils import matcher

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

MAX_UPLOAD_MB = 8
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_MB * 1024 * 1024


@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/roles', methods=['GET'])
def get_roles():
    """Return the full role catalog (id, title, tagline, required skills)."""
    out = []
    for role_id, role in ROLES.items():
        out.append({
            'roleId': role_id,
            'title': role['title'],
            'tagline': role['tagline'],
            'skills': [
                {'id': s['id'], 'name': SKILL_DB['skills'][s['id']]['name'], 'weight': s['weight']}
                for s in role['skills']
            ],
        })
    return jsonify(out)


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Accepts multipart/form-data:
      - resume_file (optional file) OR resume_text (string)
      - role_id (optional, selects from the built-in catalog)
      - job_description (optional, free-text JD — used if role_id absent)
    Returns match score, ATS score + breakdown, skill gap roadmap,
    and a ranking of every role against the candidate's detected skills.
    """
    resume_text = request.form.get('resume_text', '').strip()
    role_id = request.form.get('role_id', '').strip()
    job_description = request.form.get('job_description', '').strip()

    if not resume_text:
        file = request.files.get('resume_file')
        if not file or file.filename == '':
            return jsonify({'error': 'Provide resume_text or upload resume_file.'}), 400
        try:
            resume_text = extract_text(file.filename, file.read())
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    if not resume_text or len(resume_text.strip()) < 20:
        return jsonify({'error': 'Could not read enough text from the resume provided.'}), 400

    if not role_id and not job_description:
        return jsonify({'error': 'Provide either role_id or job_description.'}), 400

    analysis = analyze_resume_text(resume_text)

    if role_id:
        if role_id not in ROLES:
            return jsonify({'error': f'Unknown role_id "{role_id}". See /api/roles for valid ids.'}), 400
        role_title = ROLES[role_id]['title']
        role_skills_spec = ROLES[role_id]['skills']
    else:
        role_title = 'Custom job description'
        role_skills_spec = matcher.build_role_from_job_text(job_description)
        if not role_skills_spec:
            return jsonify({'error': 'No recognizable skill keywords were found in that job description.'}), 400

    match_result = matcher.score_against_role_skills(analysis['skills'], role_skills_spec)
    ats = matcher.ats_score(analysis, match_result['percent'])
    roadmap = matcher.build_roadmap(match_result['missing'])
    ranked = matcher.rank_all_roles(analysis['skills'])

    return jsonify({
        'roleTitle': role_title,
        'roleId': role_id or None,
        'contact': analysis['contact'],
        'sections': analysis['sections'],
        'wordCount': analysis['words'],
        'detectedSkills': [SKILL_DB['skills'][s]['name'] for s in analysis['skills']],
        'match': match_result,
        'ats': ats,
        'roadmap': roadmap,
        'roleRanking': ranked,
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'roles': len(ROLES), 'skills': len(SKILL_DB['skills'])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
