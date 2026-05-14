from fastapi import APIRouter, HTTPException

from database import SessionLocal
from models import Revision, SchoolPage

router = APIRouter(
    prefix="/revisions",
    tags=["revisions"]
)


# 수정 기록 조회
@router.get("/")
def get_revisions():
    db = SessionLocal()

    revisions = db.query(Revision).all()

    return revisions


# 롤백
@router.post("/{revision_id}/rollback")
def rollback_revision(revision_id: int):
    db = SessionLocal()

    revision = (
        db.query(Revision)
        .filter(Revision.id == revision_id)
        .first()
    )

    if not revision:
        raise HTTPException(
            status_code=404,
            detail="revision 없음"
        )

    page = (
        db.query(SchoolPage)
        .filter(SchoolPage.id == revision.school_id)
        .first()
    )

    if not page:
        raise HTTPException(
            status_code=404,
            detail="학교 페이지 없음"
        )

    page.content = revision.old_content

    db.commit()

    return {
        "message": "롤백 완료"
    }