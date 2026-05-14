from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from database import SessionLocal
from models import SchoolPage, Revision

router = APIRouter(
    prefix="/school",
    tags=["school"]
)


class SchoolUpdate(BaseModel):
    title: str
    content: str


# 학교 정보 조회
@router.get("/")
def get_school_page():
    db = SessionLocal()

    page = db.query(SchoolPage).first()

    if not page:
        return {
            "message": "학교 정보가 아직 없습니다"
        }

    return page


# 학교 정보 수정
@router.put("/")
def update_school_page(data: SchoolUpdate):
    db = SessionLocal()

    page = db.query(SchoolPage).first()

    # 최초 생성
    if not page:
        page = SchoolPage(
            title=data.title,
            content=data.content
        )

        db.add(page)
        db.commit()
        db.refresh(page)

        db.execute(
            text("""
                INSERT INTO school_pages_fts
                (rowid, title, content)
                VALUES (:id, :title, :content)
            """),
            {
                "id": page.id,
                "title": page.title,
                "content": page.content
            }
        )

        db.commit()

        return {
            "message": "학교 정보 생성 완료"
        }

    # 수정 기록 저장
    revision = Revision(
        school_id=page.id,
        old_content=page.content,
        new_content=data.content
    )

    db.add(revision)

    page.title = data.title
    page.content = data.content

    db.commit()

    db.execute(
        text("""
            UPDATE school_pages_fts
            SET title=:title,
                content=:content
            WHERE rowid=:id
        """),
        {
            "id": page.id,
            "title": page.title,
            "content": page.content
        }
    )

    db.commit()

    return {
        "message": "학교 정보 수정 완료"
    }


# 검색
@router.get("/search")
def search_school(q: str):
    db = SessionLocal()

    result = db.execute(
        text("""
            SELECT rowid, title, content
            FROM school_pages_fts
            WHERE school_pages_fts MATCH :query
        """),
        {
            "query": q
        }
    )

    rows = result.fetchall()

    return [dict(row._mapping) for row in rows]