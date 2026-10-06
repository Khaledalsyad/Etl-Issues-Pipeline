import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is required")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is required")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

HOURS_TIME = int(os.getenv("HOURS_TIME", os.getenv("HOURES_TIME", "0")))
MINUTE_TIME = int(os.getenv("MINUTE_TIME", os.getenv("MINTUE_TIME", "0")))
TIME_ZONE = os.getenv("TIME_ZONE", "UTC")

GITHUB_ORGANIZATION= os.getenv("GITHUB_ORGANIZATION")

if not GITHUB_ORGANIZATION:
    raise ValueError(f"{GITHUB_ORGANIZATION} Not Found")

GITHUB_REPOSITORY= os.getenv("GITHUB_REPOSITORY")

if not GITHUB_REPOSITORY:
    raise ValueError(f"{GITHUB_REPOSITORY} Not Found")
