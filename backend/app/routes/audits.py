import json
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session, selectinload

from ..config import settings
from ..database import get_db
from ..models import Audit, Workflow
from ..schemas import AuditCreate, AuditOut
from ..services.audit_service import run_audit

router = APIRouter()

def get_audit(db: Session, audit_id: int):
    return db.query(Audit).options(
        selectinload(Audit.workflows),
        selectinload(Audit.findings),
        selectinload(Audit.recommendations),
    ).filter(Audit.id == audit_id).first()

@router.post("", response_model=AuditOut)
def create_audit(payload: AuditCreate, db: Session = Depends(get_db)):
    audit = Audit(project_name=payload.project_name, description=payload.description)
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return get_audit(db, audit.id)

@router.get("", response_model=list[AuditOut])
def list_audits(db: Session = Depends(get_db)):
    return db.query(Audit).options(
        selectinload(Audit.workflows),
        selectinload(Audit.findings),
        selectinload(Audit.recommendations),
    ).order_by(Audit.created_at.desc()).all()

@router.get("/{audit_id}", response_model=AuditOut)
def get_audit_detail(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit(db, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")
    return audit

@router.post("/{audit_id}/workflow", response_model=AuditOut)
async def upload_workflow(
    audit_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    audit = db.get(Audit, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")

    if not file.filename.lower().endswith(".json"):
        raise HTTPException(400, "Please upload an n8n workflow JSON file.")

    raw = await file.read()
    if len(raw) > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(413, "Workflow file is too large.")

    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(400, "Invalid JSON file.")

    if not isinstance(data, dict) or not isinstance(data.get("nodes", []), list):
        raise HTTPException(400, "The JSON does not look like an n8n workflow.")

    safe_name = Path(file.filename).name
    folder = settings.storage_path / str(audit_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / safe_name
    path.write_bytes(raw)

    workflow = Workflow(
        audit_id=audit_id,
        name=data.get("name") or safe_name,
        raw_json_path=str(path),
    )
    db.add(workflow)
    audit.status = "workflow_uploaded"
    db.commit()

    return get_audit(db, audit_id)

@router.post("/{audit_id}/start", response_model=AuditOut)
def start_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit(db, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")
    if not audit.workflows:
        raise HTTPException(400, "Upload at least one workflow before starting the audit.")

    try:
        return run_audit(db, audit)
    except Exception as exc:
        audit.status = "failed"
        db.commit()
        raise HTTPException(500, f"Audit failed: {str(exc)}")

@router.get("/{audit_id}/findings")
def findings(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit(db, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")
    return audit.findings

@router.get("/{audit_id}/recommendations")
def recommendations(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit(db, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")
    return audit.recommendations

@router.get("/{audit_id}/report")
def report(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit(db, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")

    return {
        "audit_id": audit.id,
        "project_name": audit.project_name,
        "summary": audit.workflow_summary,
        "overall_score": audit.overall_score,
        "risk_level": audit.risk_level,
        "production_readiness": audit.production_readiness,
        "workflows": audit.workflows,
        "findings": audit.findings,
        "recommendations": audit.recommendations,
    }

@router.delete("/{audit_id}")
def delete_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = db.get(Audit, audit_id)
    if not audit:
        raise HTTPException(404, "Audit not found")
    db.delete(audit)
    db.commit()
    return {"message": "Audit deleted successfully"}
