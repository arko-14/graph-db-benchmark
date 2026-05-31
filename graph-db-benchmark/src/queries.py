CREATE_CONSTRAINTS_NEO4J = [
    "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
    "CREATE CONSTRAINT company_id IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT post_id IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE",
]

CREATE_INDEXES_MEMGRAPH = [
    "CREATE INDEX ON :User(id)",
    "CREATE INDEX ON :Company(id)",
    "CREATE INDEX ON :Skill(id)",
    "CREATE INDEX ON :Post(id)",
]

CLEAR_DB = """
MATCH (n)
DETACH DELETE n
"""

QUERY_USER_BY_ID = """
MATCH (u:User {id: $user_id})
RETURN u.id AS id, u.name AS name, u.age AS age
"""

QUERY_USER_SKILLS = """
MATCH (u:User {id: $user_id})-[:HAS_SKILL]->(s:Skill)
RETURN s.name AS skill
"""

QUERY_FRIENDS_OF_FRIENDS = """
MATCH (u:User {id: $user_id})-[:FOLLOWS]->(:User)-[:FOLLOWS]->(fof:User)
WHERE fof.id <> u.id
RETURN DISTINCT fof.id AS user_id
LIMIT 50
"""

QUERY_SIMILAR_USERS_BY_SKILL = """
MATCH (u:User {id: $user_id})-[:HAS_SKILL]->(s:Skill)<-[:HAS_SKILL]-(other:User)
WHERE other.id <> u.id
RETURN other.id AS user_id, count(s) AS shared_skills
ORDER BY shared_skills DESC
LIMIT 20
"""

QUERY_POSTS_BY_COMPANY_EMPLOYEES = """
MATCH (c:Company {id: $company_id})<-[:WORKS_AT]-(u:User)-[:CREATED]->(p:Post)
RETURN p.id AS post_id, p.title AS title
LIMIT 50
"""

BENCHMARK_QUERIES = {
    "user_by_id": QUERY_USER_BY_ID,
    "user_skills_1hop": QUERY_USER_SKILLS,
    "friends_of_friends_2hop": QUERY_FRIENDS_OF_FRIENDS,
    "similar_users_aggregation": QUERY_SIMILAR_USERS_BY_SKILL,
    "posts_by_company_employees": QUERY_POSTS_BY_COMPANY_EMPLOYEES,
}