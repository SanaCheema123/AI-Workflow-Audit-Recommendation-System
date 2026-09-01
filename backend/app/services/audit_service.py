import json
from pathlib import Path

from sqlalchemy.orm import Session

from ..models import Audit, Finding, Recommendation, Workflow
from .workflow_parser import parse_n8n_workflow
from .rule_auditor import audit_rules, calculate_score, risk_from_score, readiness_from_score
from .gemini_service import analyze_with_gemini

def run_audit(db: Session, audit: Audit) -> Audit:
    audit.status = "analyzing"

    summaries = []
    rule_findings = []

    for workflow in audit.workflows:
        try:
            data = json.loads(Path(workflow.raw_json_path).read_text(encoding="utf-8"))
        except Exception:
            continue

        summary = parse_n8n_workflow(data)
        workflow.node_count = summary["node_count"]
        workflow.trigger_count = summary["trigger_count"]
        workflow.ai_node_count = summary["ai_node_count"]
        workflow.integration_count = summary["integration_count"]
        workflow.connection_count = summary["connection_count"]
        workflow.parsed_summary = json.dumps(summary)
        summaries.append(summary)
        rule_findings.extend(audit_rules(summary))

    ai_context = {
        "project_name": audit.project_name,
        "description": audit.description,
        "workflows": summaries,
        "rule_findings": rule_findings,
    }

    ai_result = analyze_with_gemini(ai_context)

    # Replace previous generated results so rerunning an audit does not duplicate records.
    db.query(Finding).filter(Finding.audit_id == audit.id).delete()
    db.query(Recommendation).filter(Recommendation.audit_id == audit.id).delete()

    seen = set()
    for item in rule_findings + ai_result.get("findings", []):
        key = (item.get("workflow_name",""), item.get("category",""), item.get("title","").lower())
        if key in seen:
            continue
        seen.add(key)
        db.add(Finding(audit_id=audit.id, **{
            k: item.get(k, "") for k in
            ("workflow_name","category","severity","title","detail","evidence","impact")
        }))

    seen_rec = set()
    
    for item in ai_result.get("recommendations", []):
        key = (item.get("category",""), item.get("title","").lower())
        if key in seen_rec:
            continue
        seen_rec.add(key)
        db.add(Recommendation(audit_id=audit.id, **{
            k: item.get(k, "") for k in
            ("priority","category","title","action","rationale","expected_impact")
        }))

    score = 100
    if summaries:
        scores = [calculate_score([f for f in rule_findings if f["workflow_name"] == s["name"]], s) for s in summaries]
        score = round(sum(scores) / len(scores))
  

    audit.overall_score = score
    audit.risk_level = risk_from_score(score)
    audit.production_readiness = readiness_from_score(score)
    audit.workflow_summary = ai_result.get("summary", "Audit completed using structural rules and AI-assisted review.")
    audit.status = "completed"

    db.commit()
    db.refresh(audit)
    return audit
