from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from skills_extractor import extract_skills, normalize_skill

model = SentenceTransformer("all-MiniLM-L6-v2")


def analyze_resume(resume_text, jd_text):

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    resume_skills = list(set([normalize_skill(s) for s in resume_skills]))
    jd_skills = list(set([normalize_skill(s) for s in jd_skills]))

    matched = []
    missing = []

    if not jd_skills:
        return None

    resume_embeddings = model.encode(resume_skills)
    jd_embeddings = model.encode(jd_skills)

    for i, jd_skill in enumerate(jd_skills):

        similarity = cosine_similarity(
            [jd_embeddings[i]], resume_embeddings
        ).max()

        if similarity > 0.6:
            matched.append(jd_skill)
        else:
            missing.append(jd_skill)

    skill_score = len(matched) / len(jd_skills)

    keyword_count = 0
    for skill in jd_skills:
        keyword_count += resume_text.lower().count(skill)

    keyword_score = min(keyword_count / 10, 1)

    sections = ["education","skills","projects","experience","certifications"]

    structure_score = sum(
        [1 for s in sections if s in resume_text.lower()]
    ) / len(sections)

    ats_score = (
        0.5 * skill_score +
        0.3 * structure_score +
        0.2 * keyword_score
    )

    return {

        "ats_score": round(ats_score * 100,2),

        "skill_score": round(skill_score * 100,2),

        "keyword_score": round(keyword_score * 100,2),

        "structure_score": round(structure_score * 100,2),

        "matched": sorted(matched),

        "missing": sorted(missing),

        "resume_skills": sorted(resume_skills)
    }