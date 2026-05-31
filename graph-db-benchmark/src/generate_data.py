import json
import random
from pathlib import Path
from faker import Faker
from tqdm import tqdm

from config import (
    NUM_USERS,
    NUM_COMPANIES,
    NUM_SKILLS,
    NUM_POSTS,
    NUM_FOLLOWS,
)

fake = Faker()

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def generate_users():
    users = []

    for i in tqdm(range(NUM_USERS), desc="Generating users"):
        users.append({
            "id": f"user_{i}",
            "name": fake.name(),
            "age": random.randint(18, 60),
            "city": fake.city(),
        })

    return users


def generate_companies():
    companies = []

    for i in tqdm(range(NUM_COMPANIES), desc="Generating companies"):
        companies.append({
            "id": f"company_{i}",
            "name": fake.company(),
            "industry": random.choice([
                "AI",
                "Healthcare",
                "FinTech",
                "EdTech",
                "Energy",
                "SaaS",
            ]),
        })

    return companies


def generate_skills():
    base_skills = [
        "Python", "FastAPI", "Neo4j", "Memgraph", "Docker",
        "Kubernetes", "Machine Learning", "LLM", "RAG", "SQL",
        "Redis", "Kafka", "System Design", "React", "Node.js",
        "LangChain", "LangGraph", "Pandas", "PyTorch", "AWS",
    ]

    skills = []

    for i in tqdm(range(NUM_SKILLS), desc="Generating skills"):
        if i < len(base_skills):
            name = base_skills[i]
        else:
            name = f"Skill_{i}"

        skills.append({
            "id": f"skill_{i}",
            "name": name,
        })

    return skills


def generate_posts(users):
    posts = []

    for i in tqdm(range(NUM_POSTS), desc="Generating posts"):
        user = random.choice(users)

        posts.append({
            "id": f"post_{i}",
            "title": fake.sentence(nb_words=6),
            "likes": random.randint(0, 5000),
            "creator_id": user["id"],
        })

    return posts


def generate_relationships(users, companies, skills, posts):
    relationships = {
        "works_at": [],
        "has_skill": [],
        "follows": [],
        "created": [],
    }

    user_ids = [u["id"] for u in users]
    company_ids = [c["id"] for c in companies]
    skill_ids = [s["id"] for s in skills]

    for user in tqdm(users, desc="Generating WORKS_AT"):
        relationships["works_at"].append({
            "user_id": user["id"],
            "company_id": random.choice(company_ids),
        })

    for user in tqdm(users, desc="Generating HAS_SKILL"):
        selected_skills = random.sample(skill_ids, random.randint(3, 8))
        for skill_id in selected_skills:
            relationships["has_skill"].append({
                "user_id": user["id"],
                "skill_id": skill_id,
            })

    follow_pairs = set()

    while len(follow_pairs) < NUM_FOLLOWS:
        source = random.choice(user_ids)
        target = random.choice(user_ids)

        if source != target:
            follow_pairs.add((source, target))

    for source, target in tqdm(follow_pairs, desc="Generating FOLLOWS"):
        relationships["follows"].append({
            "source_id": source,
            "target_id": target,
        })

    for post in tqdm(posts, desc="Generating CREATED"):
        relationships["created"].append({
            "user_id": post["creator_id"],
            "post_id": post["id"],
        })

    return relationships


def save_json(filename, data):
    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    users = generate_users()
    companies = generate_companies()
    skills = generate_skills()
    posts = generate_posts(users)
    relationships = generate_relationships(users, companies, skills, posts)

    save_json("users.json", users)
    save_json("companies.json", companies)
    save_json("skills.json", skills)
    save_json("posts.json", posts)
    save_json("relationships.json", relationships)

    print("Synthetic data generated inside ./data")


if __name__ == "__main__":
    main()