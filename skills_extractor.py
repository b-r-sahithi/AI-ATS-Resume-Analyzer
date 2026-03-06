import re
from skills_db import SKILLS_DB, SKILL_SYNONYMS


def normalize_skill(skill):

    skill = skill.lower()

    if skill in SKILL_SYNONYMS:
        return SKILL_SYNONYMS[skill]

    return skill


def extract_skills(text):

    text = text.lower()

    found_skills = set()

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.add(normalize_skill(skill))

    return sorted(list(found_skills))