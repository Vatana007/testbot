from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"), override=True)

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

# Render provides postgres:// — SQLAlchemy requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fall back to SQLite if no DATABASE_URL is set
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./school.db"

# Resolve relative SQLite paths relative to the backend directory to prevent directory-dependent db split-brain
if DATABASE_URL.startswith("sqlite:///./"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = DATABASE_URL.split("sqlite:///./", 1)[1]
    DATABASE_URL = f"sqlite:///{os.path.join(base_dir, db_name)}"
elif DATABASE_URL.startswith("sqlite:///") and not DATABASE_URL.startswith("sqlite:////") and not DATABASE_URL.startswith("sqlite:///memory:"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = DATABASE_URL.split("sqlite:///", 1)[1]
    if not os.path.isabs(db_name):
        DATABASE_URL = f"sqlite:///{os.path.join(base_dir, db_name)}"

if DATABASE_URL.startswith("http"):
    raise RuntimeError(
        "DATABASE_URL must be a PostgreSQL connection string, not the Supabase API URL. "
        "Use the Supabase Database connection URI, for example: "
        "postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres"
    )

db_url = make_url(DATABASE_URL)
print(f"[DB] Using: {db_url.drivername}://{db_url.host or 'local'}/{db_url.database or ''}")

# Optimize connection pooling for production database (PostgreSQL/Supabase)
# While SQLite uses single-thread mode, PostgreSQL pools connections to handle high concurrency.
engine_kwargs = {}
if "sqlite" in DATABASE_URL:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_size": 50,          # Maintain up to 50 persistent connections
        "max_overflow": 30,       # Allow up to 30 temporary overflow connections
        "pool_timeout": 30,       # Wait up to 30 seconds for a connection from the pool
        "pool_recycle": 1800,     # Recycle connections after 30 minutes to avoid staleness
        "pool_pre_ping": True,    # Health check connection health before executing queries
    })

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
