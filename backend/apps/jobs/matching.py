import re

SYNONYMS = {
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "reactjs": "react",
    "react": "react",
    "next": "next.js",
    "nextjs": "next.js",
    "next.js": "next.js",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "py": "python",
    "python": "python",
}


def normalize(token):
    token = token.strip().lower()
    return SYNONYMS.get(token, token)


def skill_set(profile):
    return {normalize(skill.name) for skill in profile.skills.all() if skill.name.strip()}


def tokenize(text):
    return {normalize(token) for token in re.split(r"[^a-zA-Z0-9+#.]+", (text or "").lower()) if len(token) > 1}


def match_job(profile, job):
    skills = skill_set(profile)
    tags = {normalize(part) for part in (job.tags or "").split(",") if part.strip()}
    requirements = tokenize(job.requirements)
    title = tokenize(job.title)
    description = tokenize(job.description)
    corpus = tags | requirements | title | description
    matched = sorted(skill for skill in skills if skill in corpus)
    missing = sorted(tag for tag in tags if tag not in skills)

    skill_score = 0 if not tags and not requirements else round(100 * len(matched) / max(len(tags or requirements), 1))
    title_hits = sorted(skill for skill in skills if skill in title)
    title_score = 100 if title_hits else 0
    city = (profile.city or "").lower()
    location_score = 100 if city and city in (job.location or "").lower() else 40 if job.workplace == "remote" else 20
    coverage = 0 if not requirements else round(100 * len(skills & requirements) / len(requirements))

    score = round(skill_score * 0.5 + title_score * 0.15 + location_score * 0.15 + coverage * 0.2)
    score = max(5, min(score, 99))
    if score >= 80:
        recommendation = "Strong match. Apply this week and mention the matched skills in the cover letter."
    elif score >= 60:
        recommendation = "Good match. Close one missing skill or show a related project before applying."
    elif score >= 40:
        recommendation = "Partial match. Save the role and fill the missing tags first."
    else:
        recommendation = "Low overlap. Keep it saved only if you plan to learn the missing skills."
    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "summary": f"{len(matched)} skills overlap with {job.title}.",
        "recommendation": recommendation,
        "breakdown": {
            "skills": skill_score,
            "title": title_score,
            "location": location_score,
            "requirements": coverage,
        },
    }
