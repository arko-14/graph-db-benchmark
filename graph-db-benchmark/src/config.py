import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_BOLT_PORT = os.getenv("NEO4J_BOLT_PORT", "7687")
MEMGRAPH_BOLT_PORT = os.getenv("MEMGRAPH_BOLT_PORT", "7688")

NEO4J_URI = os.getenv("NEO4J_URI", f"bolt://localhost:{NEO4J_BOLT_PORT}")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

MEMGRAPH_URI = os.getenv("MEMGRAPH_URI", f"bolt://localhost:{MEMGRAPH_BOLT_PORT}")
MEMGRAPH_USER = os.getenv("MEMGRAPH_USER", "")
MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD", "")

NUM_USERS = int(os.getenv("NUM_USERS", 5000))
NUM_COMPANIES = int(os.getenv("NUM_COMPANIES", 200))
NUM_SKILLS = int(os.getenv("NUM_SKILLS", 100))
NUM_POSTS = int(os.getenv("NUM_POSTS", 10000))
NUM_FOLLOWS = int(os.getenv("NUM_FOLLOWS", 25000))
