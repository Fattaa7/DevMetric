# test_db_connection.py

from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql+psycopg2://devmetrics:devmetrics@localhost:5432/devmetrics_db"
)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Connection successful:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
