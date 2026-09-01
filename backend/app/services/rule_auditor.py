from typing import Any


# =========================================================
# SEVERITY CONFIGURATION
# =========================================================

SEVERITY_SCORE = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


SEVERITY_PENALTY = {
    "critical": 24,
    "high": 14,
    "medium": 7,
    "low": 3,
}


# =========================================================
# FINDING BUILDER
# =========================================================

def make_finding(
    workflow_name: str,
    category: str,
    severity: str,
    title: str,
    detail: str,
    evidence: str,
    impact: str,
) -> dict[str, Any]:

    return {
        "workflow_name": workflow_name,
        "category": category,
        "severity": severity,
        "title": title,
        "detail": detail,
        "evidence": evidence,
        "impact": impact,
    }


# =========================================================
# DEDUPLICATION
# =========================================================

def add_finding(
    findings: list[dict[str, Any]],
    finding: dict[str, Any],
) -> None:

    key = (
        finding["category"],
        finding["title"].lower(),
    )

    existing = {
        (
            item["category"],
            item["title"].lower(),
        )
        for item in findings
    }

    if key not in existing:
        findings.append(finding)


# =========================================================
# MAIN RULE AUDITOR
# =========================================================

def audit_rules(summary: dict[str, Any]) -> list[dict[str, Any]]:

    findings: list[dict[str, Any]] = []

    name = summary.get("name", "Unnamed Workflow")

    # -----------------------------------------------------
    # NORMALIZE VALUES
    # -----------------------------------------------------

    node_count = summary.get("node_count", 0)
    trigger_count = summary.get("trigger_count", 0)
    ai_node_count = summary.get("ai_node_count", 0)
    integration_count = summary.get("integration_count", 0)
    connection_count = summary.get("connection_count", 0)
    branch_count = summary.get("branch_count", 0)

    error_or_retry_count = summary.get(
        "error_or_retry_count",
        0,
    )

    approval_count = summary.get(
        "approval_count",
        0,
    )

    validation_count = summary.get(
        "validation_count",
        0,
    )

    webhook_count = summary.get(
        "webhook_count",
        0,
    )

    logging_count = summary.get(
        "logging_count",
        0,
    )

    timeout_count = summary.get(
        "timeout_count",
        0,
    )

    credential_count = summary.get(
        "credential_count",
        0,
    )

    # =====================================================
    # BASIC WORKFLOW VALIDATION
    # =====================================================

    if node_count == 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "critical",
                "Workflow contains no nodes",
                "The supplied workflow has no executable nodes to audit.",
                "node_count=0",
                "The workflow cannot perform its intended automation.",
            ),
        )

        return findings

    # =====================================================
    # ARCHITECTURE
    # =====================================================

    # Too many nodes
    if node_count >= 50:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "high",
                "Workflow complexity is very high",
                (
                    "The workflow contains a large number of nodes "
                    "and may contain too many responsibilities in "
                    "a single execution graph."
                ),
                f"node_count={node_count}",
                (
                    "High structural complexity increases maintenance "
                    "cost, debugging difficulty, and failure diagnosis time."
                ),
            ),
        )

    elif node_count >= 30:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "medium",
                "Workflow complexity is high",
                (
                    "A large node count can make automation harder "
                    "to understand, maintain, and recover."
                ),
                f"node_count={node_count}",
                (
                    "Maintenance cost and failure diagnosis can increase "
                    "as the workflow grows."
                ),
            ),
        )

    # Many branches
    if branch_count >= 12:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "high",
                "Workflow contains excessive branching",
                (
                    "The workflow contains many execution branches "
                    "that may represent tightly coupled responsibilities."
                ),
                f"branch_count={branch_count}",
                (
                    "Highly branched workflows are harder to reason about, "
                    "test, monitor, and modify safely."
                ),
            ),
        )

    elif branch_count >= 8:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "medium",
                "Workflow contains many branches",
                (
                    "Multiple branches increase execution-path complexity "
                    "and should be checked for duplicated logic."
                ),
                f"branch_count={branch_count}",
                (
                    "Complex execution paths can make changes "
                    "and troubleshooting harder."
                ),
            ),
        )

    # No trigger
    if trigger_count == 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "low",
                "No obvious trigger detected",
                (
                    "No schedule, webhook, cron, or other trigger "
                    "node was detected by the structural scanner."
                ),
                "trigger_count=0",
                (
                    "Confirm that the workflow has an intentional "
                    "and documented invocation mechanism."
                ),
            ),
        )

    # Multiple triggers
    if trigger_count >= 4:

        add_finding(
            findings,
            make_finding(
                name,
                "Architecture",
                "medium",
                "Multiple trigger types consolidated into a single workflow",
                (
                    "Several independent entry points appear to share "
                    "one execution graph."
                ),
                f"trigger_count={trigger_count}",
                (
                    "Multiple entry paths can increase operational "
                    "complexity and make execution behavior harder to trace."
                ),
            ),
        )

    # =====================================================
    # RELIABILITY
    # =====================================================

    if integration_count > 0 and error_or_retry_count == 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Reliability",
                "high",
                "No explicit retry or error handling detected",
                (
                    "The workflow uses external or integration components "
                    "but no obvious retry or error-handling mechanism "
                    "was detected."
                ),
                (
                    f"integration_count={integration_count}, "
                    f"error_or_retry_count={error_or_retry_count}"
                ),
                (
                    "Transient API, network, or service failures may "
                    "stop execution without controlled recovery."
                ),
            ),
        )

    # Timeout protection
    if integration_count >= 3 and timeout_count == 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Reliability",
                "medium",
                "Integration timeout handling should be verified",
                (
                    "Multiple external integrations are present but "
                    "the structural workflow scan cannot confirm "
                    "explicit timeout protection."
                ),
                (
                    f"integration_count={integration_count}, "
                    f"timeout_count={timeout_count}"
                ),
                (
                    "Slow or unavailable services can block execution "
                    "and increase resource consumption."
                ),
            ),
        )

    # =====================================================
    # SECURITY
    # =====================================================

    if webhook_count > 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Security",
                "medium",
                "Webhook authentication and input verification require confirmation",
                (
                    "The workflow exposes webhook-based entry points. "
                    "The structural scan cannot prove that incoming "
                    "requests are authenticated and validated."
                ),
                f"webhook_count={webhook_count}",
                (
                    "Unverified webhook requests may allow unauthorized "
                    "workflow execution or malicious input."
                ),
            ),
        )

    # Credential usage
    if credential_count > 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Security",
                "low",
                "Credential usage should be reviewed",
                (
                    "The workflow uses credential-backed integrations. "
                    "The structural scanner cannot determine whether "
                    "credentials follow least-privilege practices."
                ),
                f"credential_count={credential_count}",
                (
                    "Overprivileged or improperly managed credentials "
                    "can increase the impact of a compromised workflow."
                ),
            ),
        )

    # =====================================================
    # AI GOVERNANCE
    # =====================================================

    if ai_node_count > 0:

        if approval_count == 0:

            add_finding(
                findings,
                make_finding(
                    name,
                    "AI Governance",
                    "medium",
                    "No human approval stage detected",
                    (
                        "AI-related processing is present but no obvious "
                        "human approval stage was detected."
                    ),
                    (
                        f"ai_node_count={ai_node_count}, "
                        f"approval_count={approval_count}"
                    ),
                    (
                        "If AI output can trigger external or irreversible "
                        "actions, unsafe output may propagate automatically."
                    ),
                ),
            )

        if validation_count == 0:

            add_finding(
                findings,
                make_finding(
                    name,
                    "AI Governance",
                    "medium",
                    "AI output validation should be verified",
                    (
                        "AI processing is present but structural analysis "
                        "cannot confirm schema validation before downstream "
                        "actions."
                    ),
                    (
                        f"ai_node_count={ai_node_count}, "
                        f"validation_count={validation_count}"
                    ),
                    (
                        "Malformed or hallucinated model output can cause "
                        "downstream failures or incorrect actions."
                    ),
                ),
            )

    # =====================================================
    # PERFORMANCE
    # =====================================================

    if node_count >= 40 and integration_count >= 8:

        add_finding(
            findings,
            make_finding(
                name,
                "Performance",
                "medium",
                "Large workflow with many external operations",
                (
                    "The workflow combines a large execution graph "
                    "with numerous external integrations."
                ),
                (
                    f"node_count={node_count}, "
                    f"integration_count={integration_count}"
                ),
                (
                    "Long execution chains and external calls may "
                    "increase latency and resource consumption."
                ),
            ),
        )

    if connection_count > node_count * 2:

        add_finding(
            findings,
            make_finding(
                name,
                "Performance",
                "low",
                "Workflow connection density is high",
                (
                    "The number of connections is relatively high "
                    "compared with the number of nodes."
                ),
                (
                    f"node_count={node_count}, "
                    f"connection_count={connection_count}"
                ),
                (
                    "Dense execution graphs may indicate unnecessary "
                    "routing complexity or repeated processing."
                ),
            ),
        )

    # =====================================================
    # COST
    # =====================================================

    if ai_node_count >= 3:

        add_finding(
            findings,
            make_finding(
                name,
                "Cost",
                "medium",
                "Multiple AI processing stages may increase execution cost",
                (
                    "The workflow contains several AI processing nodes."
                ),
                f"ai_node_count={ai_node_count}",
                (
                    "Repeated model calls can increase token usage, "
                    "latency, and provider costs."
                ),
            ),
        )

    # =====================================================
    # SCALABILITY
    # =====================================================

    if integration_count >= 10:

        add_finding(
            findings,
            make_finding(
                name,
                "Scalability",
                "medium",
                "High integration dependency count",
                (
                    "The workflow depends on many external services "
                    "or integrations."
                ),
                f"integration_count={integration_count}",
                (
                    "Increasing external dependencies can create "
                    "scaling bottlenecks and a larger failure surface."
                ),
            ),
        )

    # =====================================================
    # OBSERVABILITY
    # =====================================================

    if node_count >= 15 and logging_count == 0:

        add_finding(
            findings,
            make_finding(
                name,
                "Observability",
                "medium",
                "Workflow observability should be verified",
                (
                    "The workflow is sufficiently large to benefit "
                    "from explicit logging, monitoring, or alerting, "
                    "but no obvious observability mechanism was detected."
                ),
                (
                    f"node_count={node_count}, "
                    f"logging_count={logging_count}"
                ),
                (
                    "Poor observability can make production failures "
                    "difficult to detect and diagnose."
                ),
            ),
        )

    # =====================================================
    # MAINTAINABILITY
    # =====================================================

    if node_count >= 30 and branch_count >= 6:

        add_finding(
            findings,
            make_finding(
                name,
                "Maintainability",
                "medium",
                "Workflow may contain tightly coupled responsibilities",
                (
                    "The workflow combines a large number of nodes "
                    "with multiple execution branches."
                ),
                (
                    f"node_count={node_count}, "
                    f"branch_count={branch_count}"
                ),
                (
                    "Tightly coupled workflows are harder to modify "
                    "without introducing regressions."
                ),
            ),
        )

    return findings


# =========================================================
# SCORE CALCULATION
# =========================================================

def calculate_score(
    findings: list[dict[str, Any]],
    summary: dict[str, Any],
) -> int:

    score = 100

    severity_deductions = {
        "critical": 20,
        "high": 12,
        "medium": 5,
        "low": 2,
    }

    # Track categories so repeated findings
    # do not unfairly destroy the score.
    category_counts = {}

    for finding in findings:

        severity = str(
            finding.get("severity", "low")
        ).lower()

        category = str(
            finding.get("category", "Architecture")
        )

        deduction = severity_deductions.get(
            severity,
            0,
        )

        count = category_counts.get(
            category,
            0,
        )

        # First finding in a category:
        # full penalty
        if count == 0:

            score -= deduction

        # Second finding:
        # reduced penalty
        elif count == 1:

            score -= round(
                deduction * 0.6
            )

        # Third and later:
        # small additional penalty
        else:

            score -= round(
                deduction * 0.3
            )

        category_counts[category] = (
            count + 1
        )

    # -----------------------------------------------------
    # WORKFLOW COMPLEXITY
    # -----------------------------------------------------

    node_count = summary.get(
        "node_count",
        0,
    )

    branch_count = summary.get(
        "branch_count",
        0,
    )

    if node_count >= 50:

        score -= 5

    elif node_count >= 30:

        score -= 3

    # -----------------------------------------------------
    # BRANCH COMPLEXITY
    # -----------------------------------------------------

    if branch_count >= 12:

        score -= 3

    elif branch_count >= 8:

        score -= 2

    # -----------------------------------------------------
    # KEEP SCORE BETWEEN 0 AND 100
    # -----------------------------------------------------

    return max(
        0,
        min(
            100,
            round(score),
        ),
    )

# =========================================================
# RISK CLASSIFICATION
# =========================================================

def risk_from_score(score: int) -> str:

    if score >= 85:
        return "LOW"

    if score >= 70:
        return "MEDIUM"

    if score >= 50:
        return "HIGH"

    return "CRITICAL"


# =========================================================
# PRODUCTION READINESS
# =========================================================

def readiness_from_score(score: int) -> str:

    if score >= 85:
        return "READY WITH FINAL REVIEW"

    if score >= 70:
        return "REVIEW REQUIRED"

    return "NOT PRODUCTION READY"