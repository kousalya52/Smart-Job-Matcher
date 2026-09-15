"""
The scoring brain, mirrored from the frontend's matcher.js so the
optional Flask API produces identical results to the client-side app.
"""
from .skill_data import SKILLS, ROLES, RESOURCES
from .parser import extract_skills


def score_against_role_skills(candidate_skill_ids, role_skills):
    have = set(candidate_skill_ids)
    total_weight = 0
    got_weight = 0
    matched, missing = [], []

    for req in role_skills:
        total_weight += req['weight']
        skill = SKILLS[req['id']]
        if req['id'] in have:
            got_weight += req['weight']
            matched.append({'id': req['id'], 'name': skill['name'], 'weight': req['weight']})
        else:
            missing.append({'id': req['id'], 'name': skill['name'], 'weight': req['weight']})

    percent = round((got_weight / total_weight) * 100) if total_weight else 0
    matched.sort(key=lambda s: -s['weight'])
    missing.sort(key=lambda s: -s['weight'])
    return {'percent': percent, 'matched': matched, 'missing': missing}


def rank_all_roles(candidate_skill_ids):
    results = []
    for role_id, role in ROLES.items():
        r = score_against_role_skills(candidate_skill_ids, role['skills'])
        results.append({'roleId': role_id, 'title': role['title'], 'tagline': role['tagline'], 'percent': r['percent']})
    results.sort(key=lambda r: -r['percent'])
    return results


def build_role_from_job_text(jd_text: str):
    skill_ids = extract_skills(jd_text)
    return [{'id': sid, 'weight': 2} for sid in skill_ids]


def priority_label(weight: int) -> str:
    if weight >= 3:
        return 'Must-have'
    if weight >= 2:
        return 'Important'
    return 'Good to have'


def build_roadmap(missing_skills):
    roadmap = []
    for m in missing_skills[:8]:
        res = RESOURCES.get(m['id'], {'platform': 'Official documentation', 'action': 'Study the fundamentals and build one small project'})
        roadmap.append({
            'skill': m['name'],
            'priority': priority_label(m['weight']),
            'weight': m['weight'],
            'platform': res['platform'],
            'action': res['action'],
        })
    return roadmap


def ats_score(analysis: dict, match_percent: int):
    checks = []
    score = 0

    has_email = bool(analysis['contact']['email'])
    has_phone = bool(analysis['contact']['phone'])
    contact_pts = (5 if has_email else 0) + (5 if has_phone else 0)
    score += contact_pts
    checks.append({
        'label': 'Contact details findable',
        'pass': contact_pts == 10,
        'points': contact_pts, 'max': 10,
        'tip': 'Email and phone number are both present and machine-readable.' if contact_pts == 10 else
               'Add a clear email and 10-digit phone number near the top of the resume.',
    })

    sections = analysis['sections']
    sections_found = sum(1 for v in sections.values() if v)
    section_pts = sections_found * 5
    score += section_pts
    missing_sections = [k for k, v in sections.items() if not v]
    checks.append({
        'label': 'Standard resume sections present',
        'pass': len(missing_sections) == 0,
        'points': section_pts, 'max': 25,
        'tip': 'All key sections (Education, Skills, Experience, Certifications) were detected.' if not missing_sections
               else f"Add or clearly label: {', '.join(missing_sections)}.",
    })

    wc = analysis['words']
    wc_good = 250 <= wc <= 900
    wc_pts = 15 if wc_good else (5 if wc < 250 else 8)
    score += wc_pts
    checks.append({
        'label': 'Resume length is scanner-friendly',
        'pass': wc_good,
        'points': wc_pts, 'max': 15,
        'tip': f'{wc} words is a healthy length for one or two pages.' if wc_good else
               (f'Only {wc} words found — add more detail on projects and impact.' if wc < 250 else
                f'{wc} words is on the longer side — tighten it to the most relevant points.'),
    })

    bullet_lines = analysis['structure']['bulletLines']
    verb_hits = analysis['structure']['verbHits']
    structure_pts = min(10, bullet_lines * 2) + min(10, verb_hits * 2)
    score += structure_pts
    checks.append({
        'label': 'Uses bullet points and action verbs',
        'pass': structure_pts >= 14,
        'points': structure_pts, 'max': 20,
        'tip': 'Good use of bullet points and strong action verbs like "built" or "led".' if structure_pts >= 14 else
               'Rewrite experience/project lines as bullet points starting with action verbs (Built, Developed, Automated).',
    })

    keyword_pts = round((match_percent / 100) * 30)
    score += keyword_pts
    checks.append({
        'label': 'Keyword match with target role',
        'pass': match_percent >= 50,
        'points': keyword_pts, 'max': 30,
        'tip': 'Resume keywords line up well with what the target role is scanning for.' if match_percent >= 50 else
               'Mirror more of the exact skill keywords used in the job description or role profile.',
    })

    return {'score': min(100, score), 'checks': checks}
