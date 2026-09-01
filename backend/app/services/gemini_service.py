
import json
import time

from google import genai
from google.genai import types

from ..config import settings


# =========================================================
# FALLBACK RECOMMENDATION GENERATOR
# =========================================================

def generate_fallback_recommendations(audit_context: dict) -> list[dict]:
    """
    Generate practical recommendations from deterministic findings.

    This is used when Gemini is unavailable, so the audit can still
    produce useful recommendations without an AI provider.
    """

    recommendations = []
    findings = audit_context.get("rule_findings", [])

    for finding in findings:

        category = finding.get("category", "Architecture")
        severity = finding.get("severity", "medium")
        title = finding.get("title", "")
        detail = finding.get("detail", "")
        impact = finding.get("impact", "")

        # -----------------------------------------------------
        # PRIORITY
        # -----------------------------------------------------

        priority_map = {
            "critical": "P0",
            "high": "P1",
            "medium": "P2",
            "low": "P2",
        }

        priority = priority_map.get(severity.lower(), "P2")

        title_lower = title.lower()

        # -----------------------------------------------------
        # RELIABILITY — RETRY / ERROR HANDLING
        # -----------------------------------------------------

        if (
            "retry" in title_lower
            or "error handling" in title_lower
            or "failure" in title_lower
        ):

            recommendations.append({
                "priority": priority,
                "category": "Reliability",
                "title": "Add explicit retry and error handling",
                "action": (
                    "Add controlled retry logic, timeout handling, "
                    "failure branches, and an appropriate fallback "
                    "or alert path for external service failures."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Improves workflow reliability, failure recovery, "
                    "and operational resilience."
                ),
            })

        # -----------------------------------------------------
        # AI GOVERNANCE — HUMAN APPROVAL
        # -----------------------------------------------------

        elif "human approval" in title_lower:

            recommendations.append({
                "priority": priority,
                "category": "AI Governance",
                "title": "Add a human approval gate for sensitive AI actions",
                "action": (
                    "Introduce a human review or approval step before "
                    "AI-generated output is used for external, "
                    "irreversible, or high-impact actions."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Reduces the risk of incorrect or unsafe AI output "
                    "being automatically propagated."
                ),
            })

        # -----------------------------------------------------
        # AI GOVERNANCE — OUTPUT VALIDATION
        # -----------------------------------------------------

        elif "output validation" in title_lower:

            recommendations.append({
                "priority": priority,
                "category": "AI Governance",
                "title": "Validate AI output before downstream processing",
                "action": (
                    "Add structured schema validation for AI responses "
                    "and reject, repair, or route malformed output "
                    "before it reaches downstream workflow actions."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Improves AI reliability and prevents malformed, "
                    "unexpected, or unsafe model output from affecting "
                    "downstream operations."
                ),
            })

        # -----------------------------------------------------
        # ARCHITECTURE — COMPLEXITY
        # -----------------------------------------------------

        elif "complexity" in title_lower:

            recommendations.append({
                "priority": priority,
                "category": "Architecture",
                "title": "Reduce unnecessary workflow complexity",
                "action": (
                    "Review the workflow for duplicated logic, "
                    "unnecessary branches, and tightly coupled steps. "
                    "Consider splitting large responsibilities into "
                    "smaller reusable workflows."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Improves maintainability, troubleshooting, "
                    "readability, and scalability."
                ),
            })

        # -----------------------------------------------------
        # ARCHITECTURE — TRIGGER
        # -----------------------------------------------------

        elif "trigger" in title_lower:

            recommendations.append({
                "priority": priority,
                "category": "Architecture",
                "title": "Verify the workflow invocation mechanism",
                "action": (
                    "Confirm that the workflow has an intentional, "
                    "documented, and reliable trigger or invocation "
                    "mechanism."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Improves operational clarity and reduces "
                    "unexpected or uncontrolled execution behavior."
                ),
            })

        # -----------------------------------------------------
        # GENERIC FALLBACK
        # -----------------------------------------------------

        else:

            recommendations.append({
                "priority": priority,
                "category": category,
                "title": f"Address: {title}",
                "action": (
                    f"Review the identified issue and implement an "
                    f"appropriate control or architectural improvement. "
                    f"Focus specifically on: {title}."
                ),
                "rationale": (
                    f"{detail} {impact}"
                ).strip(),
                "expected_impact": (
                    "Reduces the identified workflow risk and improves "
                    "overall production readiness."
                ),
            })

    # ---------------------------------------------------------
    # REMOVE DUPLICATE RECOMMENDATIONS
    # ---------------------------------------------------------

    unique = []
    seen = set()

    for recommendation in recommendations:

        key = (
            recommendation["category"],
            recommendation["title"].lower(),
        )

        if key not in seen:
            seen.add(key)
            unique.append(recommendation)

    return unique


# =========================================================
# FALLBACK AI RESULT
# =========================================================

def fallback_ai_result(audit_context: dict) -> dict:
    """
    Fallback response used when Gemini is temporarily unavailable.

    The deterministic audit findings remain available and practical
    recommendations are generated directly from those findings.
    """

    recommendations = generate_fallback_recommendations(
        audit_context
    )

    return {
        "summary": (
            "The workflow audit was completed using deterministic "
            "structural analysis. Gemini AI-assisted analysis was "
            "temporarily unavailable, so recommendations were generated "
            "from the detected audit findings."
        ),
        "findings": [],
        "recommendations": recommendations,
    }


# =========================================================
# GEMINI AUDIT ANALYSIS
# =========================================================

def analyze_with_gemini(audit_context: dict) -> dict:
    """
    Analyze a normalized workflow using Gemini.

    Gemini failures such as temporary 503/429 errors are retried.
    If Gemini remains unavailable after all attempts, the system
    automatically falls back to deterministic recommendations.
    """

    # =====================================================
    # GEMINI API KEY CHECK
    # =====================================================

    if not settings.GEMINI_API_KEY:

        print("Gemini API key is not configured.")

        return fallback_ai_result(audit_context)

    # =====================================================
    # GEMINI CLIENT
    # =====================================================

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    # =====================================================
    # AUDIT PROMPT
    # =====================================================

    prompt = f"""
You are a senior AI automation architect performing a
pre-production workflow audit.

This is a GENERIC audit.

Do not assume the project is marketing, crime, HR,
e-commerce, finance, healthcare, or any other specific domain.

Judge only the supplied evidence.

AUDIT OBJECTIVES:

- Architecture and unnecessary complexity
- Reliability and failure recovery
- Security and credential/data exposure risks
- AI governance and output validation
- Performance and cost
- Scalability
- Observability
- Maintainability

IMPORTANT RULES:

1. Do not invent facts that are not present.
2. Distinguish evidence from inference.
3. Avoid duplicate findings already present in rule_findings.
4. Give practical recommendations.
5. Return JSON only.
6. Keep findings specific and actionable.
7. Do not make assumptions about the business domain.
8. If evidence is insufficient to confirm a risk, clearly state that
   the issue should be verified instead of presenting it as confirmed.
9. Recommendations must be directly related to identified risks.
10. Do not recommend unnecessary technologies.
11. Prefer simple, maintainable solutions.
12. Do not duplicate recommendations.

INPUT:

{json.dumps(audit_context, indent=2)}

RETURN EXACTLY:

{{
    "summary": "short professional audit summary",

    "findings": [
        {{
            "workflow_name": "string",
            "category": "Architecture|Reliability|Security|AI Governance|Performance|Cost|Scalability|Observability|Maintainability",
            "severity": "critical|high|medium|low",
            "title": "short issue",
            "detail": "explanation",
            "evidence": "specific evidence from supplied input",
            "impact": "why it matters"
        }}
    ],

    "recommendations": [
        {{
            "priority": "P0|P1|P2",
            "category": "Architecture|Reliability|Security|AI Governance|Performance|Cost|Scalability|Observability|Maintainability",
            "title": "short actionable recommendation",
            "action": "what should be changed",
            "rationale": "why this change is needed",
            "expected_impact": "expected result"
        }}
    ]
}}
"""

    # =====================================================
    # RETRY CONFIGURATION
    # =====================================================

    max_attempts = 3

    retry_delays = [2, 4]

    # =====================================================
    # GEMINI REQUEST
    # =====================================================

    for attempt in range(max_attempts):

        try:

            print(
                f"Sending workflow audit to Gemini "
                f"(attempt {attempt + 1}/{max_attempts})..."
            )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )

            # =================================================
            # RESPONSE CHECK
            # =================================================

            text = response.text or ""

            print("\n===== GEMINI RAW RESPONSE =====")
            print(text)
            print("===== END GEMINI RAW RESPONSE =====\n")

            if not text.strip():

                print("Gemini returned an empty response.")

                if attempt < max_attempts - 1:

                    wait_time = retry_delays[attempt]

                    print(
                        f"Retrying Gemini request in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return fallback_ai_result(audit_context)

            # =================================================
            # JSON PARSING
            # =================================================

            try:

                result = json.loads(text)

            except json.JSONDecodeError as exc:

                print(
                    f"Gemini returned invalid JSON: {exc}"
                )

                if attempt < max_attempts - 1:

                    wait_time = retry_delays[attempt]

                    print(
                        f"Retrying Gemini request in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return fallback_ai_result(audit_context)

            # =================================================
            # RESPONSE STRUCTURE VALIDATION
            # =================================================

            if not isinstance(result, dict):

                print(
                    "Gemini response is not a JSON object."
                )

                if attempt < max_attempts - 1:

                    wait_time = retry_delays[attempt]

                    time.sleep(wait_time)

                    continue

                return fallback_ai_result(audit_context)

            # =================================================
            # ENSURE EXPECTED KEYS
            # =================================================

            result.setdefault(
                "summary",
                "Gemini audit analysis completed."
            )

            result.setdefault(
                "findings",
                []
            )

            result.setdefault(
                "recommendations",
                []
            )

            # =================================================
            # VALIDATE LIST TYPES
            # =================================================

            if not isinstance(
                result["findings"],
                list
            ):
                result["findings"] = []

            if not isinstance(
                result["recommendations"],
                list
            ):
                result["recommendations"] = []

            # =================================================
            # SUCCESS
            # =================================================

            print(
                "Gemini audit analysis completed successfully."
            )

            return result

        # =====================================================
        # GEMINI / API ERROR
        # =====================================================

        except Exception as exc:

            error_text = str(exc)

            print(
                f"Gemini request failed "
                f"(attempt {attempt + 1}/{max_attempts}): "
                f"{error_text}"
            )

            # =================================================
            # RETRY
            # =================================================

            if attempt < max_attempts - 1:

                wait_time = retry_delays[attempt]

                print(
                    f"Retrying Gemini request in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            # =================================================
            # FINAL FALLBACK
            # =================================================

            else:

                print(
                    "Gemini remains unavailable after "
                    f"{max_attempts} attempts."
                )

                print(
                    "Continuing audit using deterministic "
                    "workflow analysis and fallback recommendations."
                )

                return fallback_ai_result(audit_context)

    # =========================================================
    # SAFETY FALLBACK
    # =========================================================

    return fallback_ai_result(audit_context)

