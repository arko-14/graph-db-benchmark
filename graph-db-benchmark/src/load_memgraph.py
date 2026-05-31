import json
from pathlib import Path
from neo4j import GraphDatabase
from tqdm import tqdm

from config import MEMGRAPH_URI
from queries import CLEAR_DB, CREATE_INDEXES_MEMGRAPH

DATA_DIR = Path("data")
BATCH_SIZE = 1000


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def run_write_batch(session, query, rows):
    session.execute_write(lambda tx: tx.run(query, rows=rows).consume())


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def main():
    driver = GraphDatabase.driver(
        MEMGRAPH_URI,
        auth=None,
    )

    users = load_json("users.json")
    companies = load_json("companies.json")
    skills = load_json("skills.json")
    posts = load_json("posts.json")
    relationships = load_json("relationships.json")

    with driver.session() as session:
        print("Clearing Memgraph...")
        session.run(CLEAR_DB)

        print("Creating Memgraph indexes...")
        for query in CREATE_INDEXES_MEMGRAPH:
            try:
                session.run(query)
            except Exception as e:
                print(f"Index may already exist or failed: {e}")

        print("Loading users...")
        for batch in tqdm(list(chunked(users, BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            CREATE (:User {
                id: row.id,
                name: row.name,
                age: row.age,
                city: row.city
            })
            """, batch)

        print("Loading companies...")
        for batch in tqdm(list(chunked(companies, BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            CREATE (:Company {
                id: row.id,
                name: row.name,
                industry: row.industry
            })
            """, batch)

        print("Loading skills...")
        for batch in tqdm(list(chunked(skills, BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            CREATE (:Skill {
                id: row.id,
                name: row.name
            })
            """, batch)

        print("Loading posts...")
        for batch in tqdm(list(chunked(posts, BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            CREATE (:Post {
                id: row.id,
                title: row.title,
                likes: row.likes
            })
            """, batch)

        print("Creating WORKS_AT relationships...")
        for batch in tqdm(list(chunked(relationships["works_at"], BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            MATCH (u:User {id: row.user_id})
            MATCH (c:Company {id: row.company_id})
            CREATE (u)-[:WORKS_AT]->(c)
            """, batch)

        print("Creating HAS_SKILL relationships...")
        for batch in tqdm(list(chunked(relationships["has_skill"], BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            MATCH (u:User {id: row.user_id})
            MATCH (s:Skill {id: row.skill_id})
            CREATE (u)-[:HAS_SKILL]->(s)
            """, batch)

        print("Creating FOLLOWS relationships...")
        for batch in tqdm(list(chunked(relationships["follows"], BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            MATCH (source:User {id: row.source_id})
            MATCH (target:User {id: row.target_id})
            CREATE (source)-[:FOLLOWS]->(target)
            """, batch)

        print("Creating CREATED relationships...")
        for batch in tqdm(list(chunked(relationships["created"], BATCH_SIZE))):
            run_write_batch(session, """
            UNWIND $rows AS row
            MATCH (u:User {id: row.user_id})
            MATCH (p:Post {id: row.post_id})
            CREATE (u)-[:CREATED]->(p)
            """, batch)

    driver.close()
    print("Memgraph load complete.")


if __name__ == "__main__":
    main()