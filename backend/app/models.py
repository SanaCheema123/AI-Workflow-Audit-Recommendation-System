from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Audit(Base):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(40), default="created")
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(30), nullable=True)
    production_readiness: Mapped[str | None] = mapped_column(String(60), nullable=True)
    workflow_summary: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)

    workflows = relationship("Workflow", back_populates="audit", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="audit", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="audit", cascade="all, delete-orphan")

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    name: Mapped[str] = mapped_column(String(250))
    node_count: Mapped[int] = mapped_column(Integer, default=0)
    trigger_count: Mapped[int] = mapped_column(Integer, default=0)
    ai_node_count: Mapped[int] = mapped_column(Integer, default=0)
    integration_count: Mapped[int] = mapped_column(Integer, default=0)
    connection_count: Mapped[int] = mapped_column(Integer, default=0)
    raw_json_path: Mapped[str] = mapped_column(String(500), default="")
    parsed_summary: Mapped[str] = mapped_column(Text, default="")

    audit = relationship("Audit", back_populates="workflows")

class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    workflow_name: Mapped[str] = mapped_column(String(250), default="")
    category: Mapped[str] = mapped_column(String(60))
    severity: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(300))
    detail: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text, default="")
    impact: Mapped[str] = mapped_column(Text, default="")

    audit = relationship("Audit", back_populates="findings")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    priority: Mapped[str] = mapped_column(String(10), default="P2")
    category: Mapped[str] = mapped_column(String(60))
    title: Mapped[str] = mapped_column(String(300))
    action: Mapped[str] = mapped_column(Text)
    rationale: Mapped[str] = mapped_column(Text, default="")
    expected_impact: Mapped[str] = mapped_column(Text, default="")

    audit = relationship("Audit", back_populates="recommendations")
