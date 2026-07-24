from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    version = conn.execute(text("SELECT version();"))
    print(version.scalar())
