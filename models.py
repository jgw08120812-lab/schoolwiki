from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


# 우리 학교 위키 페이지
class SchoolPage(Base):
    __tablename__ = "school_pages"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)


# 수정 기록
class Revision(Base):
    __tablename__ = "revisions"

    id = Column(Integer, primary_key=True, index=True)

    school_id = Column(
        Integer,
        ForeignKey("school_pages.id")
    )

    old_content = Column(Text)
    new_content = Column(Text)

    edited_at = Column(
        DateTime,
        default=datetime.utcnow
    )