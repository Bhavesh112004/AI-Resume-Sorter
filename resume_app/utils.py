import re
import nltk
from nltk import word_tokenize,pos_tag,ne_chunk
from nltk.tree import Tree
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Expanded known skill sets based on job roles
COMMON_SKILLS = [
    "python", "java", "c++", "html", "css", "javascript", "react",
    "node.js", "django", "flask", "sql", "mysql", "mongodb",
    "git", "github", "machine learning", "deep learning",
    "tensorflow", "pytorch", "nlp", "data analysis", "data visualization",
    "excel", "power bi", "tableau", "aws", "azure", "linux"
]

ROLE_SKILLS = {
    "Data Scientist": [
        "python", "r", "sql", "pandas", "numpy", "matplotlib", "seaborn",
        "tensorflow", "keras", "pytorch", "scikit-learn", "data visualization",
        "machine learning", "deep learning", "statistics", "nlp",
        "power bi", "tableau"
    ],
    "Full Stack Developer": [
        "javascript", "react", "node.js", "express", "mongodb", "mysql", "html",
        "css", "django", "flask", "git", "docker", "rest api", "graphql", "typescript"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react", "redux", "typescript", "bootstrap",
        "tailwind", "vue.js", "next.js", "angular", "figma"
    ],
    "Backend Developer": [
        "python", "django", "flask", "node.js", "express", "java", "spring",
        "mysql", "postgresql", "mongodb", "rest api", "graphql", "docker", "redis"
    ]
}

def extract_basic_info(text):
    info = {
        "name": None,
        "email": None,
        "phone": None,
    }

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else None

    # Extract phone number
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){1,2}\d{4}', text)
    phone = phone_match.group(0) if phone_match else None

    # Extract name using heuristics
    try:
        sentences = nltk.sent_tokenize(text)
        for sent in sentences[:5]:  # Only check first few lines
            tokens = word_tokenize(sent)
            tagged = pos_tag(tokens)
            namedEnt = ne_chunk(tagged, binary=False)

            for subtree in namedEnt:
                if type(subtree) == Tree and subtree.label() == 'PERSON':
                    name = " ".join([token for token, pos in subtree.leaves()])
                    return {'name': name, 'email': email, 'phone': phone}
    except:
        pass

    return {'name': None, 'email': email, 'phone': phone}

def extract_skills(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in word_tokens if word.isalpha() and word not in stop_words]
    extracted_skills = list(set(filtered_tokens).intersection(set(skill.lower() for skill in COMMON_SKILLS)))
    return extracted_skills

def extract_skills_from_job_description(description):
    tokens = description.lower().split()
    return [skill for skill in COMMON_SKILLS if skill.lower() in tokens]

def match_roles(tokens):
    matched_roles = {}
    lower_tokens = set(token.lower() for token in tokens)
    for role, skills in ROLE_SKILLS.items():
        skill_matches = [skill for skill in skills if skill.lower() in lower_tokens]
        if skill_matches:
            matched_roles[role] = skill_matches
    return matched_roles


def match_jobs_to_candidate(candidate_skills, job_queryset):
    matched_jobs = []
    for job in job_queryset:
        # Normalize and split the comma-separated skills from your model
        required = [s.strip().lower() for s in job.skills_required.split(',')]

        # Calculate intersection of skills
        common_skills = set(candidate_skills) & set(required)
        match_score = len(common_skills) / len(required) if required else 0

        if match_score > 0:  # Or set a threshold like 0.3
            matched_jobs.append({
                'title': job.title,
                'role': job.role,
                'match_score': round(match_score * 100, 2),
                'matched_skills': list(common_skills),
                'missing_skills': list(set(required) - set(candidate_skills))
            })
    return sorted(matched_jobs, key=lambda x: x['match_score'], reverse=True)
