import secrets

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from sqlalchemy.orm import declarative_base

from sqlalchemy import text

from app.config import settings

def normalize_db_url(raw_url: str) -> str:
    from urllib.parse import quote_plus
    url = (raw_url or "").strip()
    if url.count("@") > 1 and "://" in url:
        proto, rest = url.split("://", 1)
        userinfo, hostinfo = rest.rsplit("@", 1)
        if ":" in userinfo:
            user, pwd = userinfo.split(":", 1)
            url = f"{proto}://{user}:{quote_plus(pwd)}@{hostinfo}"
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("mysql://") and not (url.startswith("mysql+aiomysql://") or url.startswith("mysql+asyncmy://")):
        return url.replace("mysql://", "mysql+aiomysql://", 1)
    if url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url or "sqlite+aiosqlite:///./geopulse.db"

db_url = normalize_db_url(settings.DATABASE_URL)
engine = create_async_engine(
    db_url,
    echo=False,
    pool_recycle=240,
    connect_args={"check_same_thread": False, "timeout": 30} if "sqlite" in db_url else {}
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        if "sqlite" in db_url:
            await conn.execute(text("PRAGMA journal_mode=WAL"))
            await conn.execute(text("PRAGMA busy_timeout=30000"))
        await conn.run_sync(Base.metadata.create_all)
        for col_sql in [
            "ALTER TABLE companies ADD COLUMN is_paid BOOLEAN DEFAULT 0",
            "ALTER TABLE companies ADD COLUMN payment_plan VARCHAR(100)",
            "ALTER TABLE companies ADD COLUMN paid_at DATETIME",
            "ALTER TABLE companies ADD COLUMN entity_type VARCHAR(50) DEFAULT 'company'",
            "ALTER TABLE companies ADD COLUMN professional_registry VARCHAR(120)",
            "ALTER TABLE companies ADD COLUMN payment_amount FLOAT DEFAULT 197.0",
            "ALTER TABLE companies ADD COLUMN payment_method VARCHAR(50) DEFAULT 'pix'",
            "ALTER TABLE companies ADD COLUMN whatsapp VARCHAR(60)",
            "ALTER TABLE companies ADD COLUMN email VARCHAR(150)",
            "ALTER TABLE companies ADD COLUMN photo_url VARCHAR(500)",
            "ALTER TABLE companies ADD COLUMN rating_value FLOAT",
            "ALTER TABLE companies ADD COLUMN review_count INTEGER",
            "ALTER TABLE companies ADD COLUMN services_list VARCHAR(500)",
            "ALTER TABLE companies ADD COLUMN access_token VARCHAR(64)",
            "ALTER TABLE companies ADD COLUMN payment_ref VARCHAR(100)",
            "ALTER TABLE companies ADD COLUMN last_monitored_at DATETIME",
            "ALTER TABLE companies ADD COLUMN sprint_status VARCHAR(50) DEFAULT 'pending'",
            "ALTER TABLE companies ADD COLUMN sprint_day_current INTEGER DEFAULT 0",
            "ALTER TABLE companies ADD COLUMN sprint_started_at DATETIME",
            "ALTER TABLE companies ADD COLUMN sprint_last_run_at DATETIME",
            "ALTER TABLE companies ADD COLUMN sprint_logs TEXT",
            "ALTER TABLE companies ADD COLUMN admin_notes TEXT"
        ]:
            try:
                await conn.execute(text(col_sql))
            except Exception:
                pass
        rows = (await conn.execute(text("SELECT id FROM companies WHERE access_token IS NULL OR access_token = ''"))).fetchall()
        for (cid,) in rows:
            await conn.execute(text("UPDATE companies SET access_token = :t WHERE id = :i"), {"t": secrets.token_urlsafe(24), "i": cid})
