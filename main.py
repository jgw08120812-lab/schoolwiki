from fastapi import FastAPI
from sqlalchemy import text

from database import engine
from models import Base

from routers.schools import router as school_router
from routers.revisions import router as revision_router

app = FastAPI()

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# FTS5 가상 테이블 생성
with engine.connect() as conn:
    conn.execute(text("""
        CREATE VIRTUAL TABLE IF NOT EXISTS school_pages_fts
        USING fts5(title, content)
    """))

# Router 연결
app.include_router(school_router)
app.include_router(revision_router)

@app.get("/")
def root():
    return {
        "message": "학교 위키 서버 실행 중"
    }