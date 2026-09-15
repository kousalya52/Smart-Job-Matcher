"""
Loads the shared skills/roles/resources knowledge base and builds
a fast alias -> skill_id lookup table used by the resume parser.
"""
import json
import re
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_database.json')

with open(DATA_PATH, 'r', encoding='utf-8') as f:
    SKILL_DB = json.load(f)

SKILLS = SKILL_DB['skills']
ROLES = SKILL_DB['roles']
RESOURCES = SKILL_DB['resources']


def normalize(s: str) -> str:
    """
    Normalize a term the exact same way resume text gets normalized, so
    names containing '&', '/', '.' still match ("Git & GitHub" -> "git github").
    """
    s = re.sub(r'[^a-z0-9+.#\s]', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()


def build_alias_lookup():
    """Map every normalized alias/name to its canonical skill id."""
    lookup = {}
    for skill_id, skill in SKILLS.items():
        terms = [skill_id.replace('-', ' '), skill['name']] + skill.get('aliases', [])
        for term in terms:
            key = normalize(term)
            if key:
                lookup[key] = skill_id
    return lookup


ALIAS_LOOKUP = build_alias_lookup()

# Longest terms first, so multi-word skills ("react native") match
# before their shorter substrings ("react") do.
ALL_TERMS = sorted(ALIAS_LOOKUP.keys(), key=len, reverse=True)
