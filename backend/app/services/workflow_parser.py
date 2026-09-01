from typing import Any


# =========================================================
# DETECTION HINTS
# =========================================================

AI_HINTS = (
    "agent",
    "ai",
    "openai",
    "gemini",
    "anthropic",
    "llm",
    "chat",
    "language model",
    "ollama",
    "vertex",
    "bedrock",
    "claude",
    "gpt",
)

TRIGGER_HINTS = (
    "webhook",
    "schedule",
    "cron",
    "trigger",
    "manual",
    "form",
    "polling",
)

INTEGRATION_HINTS = (
    "http",
    "api",
    "request",
    "slack",
    "discord",
    "telegram",
    "facebook",
    "instagram",
    "linkedin",
    "gmail",
    "outlook",
    "notion",
    "airtable",
    "hubspot",
    "salesforce",
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "google sheets",
    "google drive",
    "drive",
    "stripe",
    "shopify",
    "twilio",
    "sendgrid",
)

ERROR_HINTS = (
    "error",
    "stop and error",
    "retry",
    "catch",
    "exception",
    "failure",
    "error trigger",
)

APPROVAL_HINTS = (
    "approval",
    "approve",
    "human in the loop",
    "human review",
    "manual review",
    "review",
    "authorization",
)

VALIDATION_HINTS = (
    "validate",
    "validation",
    "schema",
    "json schema",
    "structured output",
    "parse json",
    "output parser",
    "guardrail",
    "guardrails",
)

WEBHOOK_HINTS = (
    "webhook",
)

TIMEOUT_HINTS = (
    "timeout",
    "time out",
)

LOGGING_HINTS = (
    "log",
    "logging",
    "logger",
    "monitor",
    "monitoring",
    "observability",
    "alert",
    "notification",
)

# =========================================================
# HELPERS
# =========================================================

def _node_text(node: dict[str, Any]) -> str:

    return " ".join(
        [
            str(node.get("name", "")),
            str(node.get("type", "")),
            str(node.get("typeVersion", "")),
        ]
    ).lower()


def _node_name(node: dict[str, Any]) -> str:

    return str(
        node.get(
            "name",
            node.get(
                "type",
                "Unnamed",
            ),
        )
    )


def _contains_hint(
    text: str,
    hints: tuple[str, ...],
) -> bool:

    return any(
        hint in text
        for hint in hints
    )


def _has_timeout_configuration(
    node: dict[str, Any],
) -> bool:

    text = _node_text(node)

    if _contains_hint(text, TIMEOUT_HINTS):
        return True

    parameters = node.get("parameters")

    if not isinstance(parameters, dict):
        return False

    parameter_text = str(parameters).lower()

    return any(
        hint in parameter_text
        for hint in TIMEOUT_HINTS
    )


def _has_credential_configuration(
    node: dict[str, Any],
) -> bool:

    if node.get("credentials"):
        return True

    parameters = node.get("parameters")

    if not isinstance(parameters, dict):
        return False

    parameter_text = str(parameters).lower()

    credential_hints = (
        "credential",
        "api key",
        "apikey",
        "authorization",
        "bearer",
        "oauth",
    )

    return any(
        hint in parameter_text
        for hint in credential_hints
    )


# =========================================================
# CONNECTION ANALYSIS
# =========================================================

def _analyze_connections(
    connections: dict[str, Any],
) -> tuple[int, int]:

    connection_count = 0
    branch_count = 0

    for _, value in connections.items():

        if not isinstance(value, dict):
            continue

        for _, outputs in value.items():

            if not isinstance(outputs, list):
                continue

            for output_group in outputs:

                if not isinstance(
                    output_group,
                    list,
                ):
                    continue

                connection_count += len(
                    output_group
                )

                if len(output_group) > 1:

                    branch_count += (
                        len(output_group) - 1
                    )

    return (
        connection_count,
        branch_count,
    )


# =========================================================
# N8N WORKFLOW PARSER
# =========================================================

def parse_n8n_workflow(
    data: dict[str, Any],
) -> dict[str, Any]:

    nodes = data.get("nodes") or []
    connections = data.get("connections") or {}

    if not isinstance(nodes, list):
        nodes = []

    if not isinstance(connections, dict):
        connections = {}

    # =====================================================
    # NODE CLASSIFICATION
    # =====================================================

    ai_nodes = []
    trigger_nodes = []
    integration_nodes = []
    error_nodes = []
    approval_nodes = []
    validation_nodes = []
    webhook_nodes = []
    timeout_nodes = []
    credential_nodes = []
    logging_nodes = []

    for node in nodes:

        if not isinstance(node, dict):
            continue

        text = _node_text(node)

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        if _contains_hint(
            text,
            AI_HINTS,
        ):
            ai_nodes.append(node)

        # -------------------------------------------------
        # TRIGGERS
        # -------------------------------------------------

        if _contains_hint(
            text,
            TRIGGER_HINTS,
        ):
            trigger_nodes.append(node)

        # -------------------------------------------------
        # INTEGRATIONS
        # -------------------------------------------------

        if _contains_hint(
            text,
            INTEGRATION_HINTS,
        ):
            integration_nodes.append(node)

        # -------------------------------------------------
        # ERROR / RETRY
        # -------------------------------------------------

        if _contains_hint(
            text,
            ERROR_HINTS,
        ):
            error_nodes.append(node)

        # -------------------------------------------------
        # APPROVAL
        # -------------------------------------------------

        if _contains_hint(
            text,
            APPROVAL_HINTS,
        ):
            approval_nodes.append(node)

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if _contains_hint(
            text,
            VALIDATION_HINTS,
        ):
            validation_nodes.append(node)

        # -------------------------------------------------
        # WEBHOOK
        # -------------------------------------------------

        if _contains_hint(
            text,
            WEBHOOK_HINTS,
        ):
            webhook_nodes.append(node)

        # -------------------------------------------------
        # TIMEOUT
        # -------------------------------------------------

        if _has_timeout_configuration(node):
            timeout_nodes.append(node)

        # -------------------------------------------------
        # CREDENTIALS
        # -------------------------------------------------

        if _has_credential_configuration(node):
            credential_nodes.append(node)

        # -------------------------------------------------
        # LOGGING / OBSERVABILITY
        # -------------------------------------------------

        if _contains_hint(
            text,
            LOGGING_HINTS,
        ):
            logging_nodes.append(node)

    # =====================================================
    # CONNECTION ANALYSIS
    # =====================================================

    (
        connection_count,
        branch_count,
    ) = _analyze_connections(
        connections
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    summary = {

        # -------------------------------------------------
        # BASIC INFORMATION
        # -------------------------------------------------

        "name": (
            data.get("name")
            or "Imported n8n Workflow"
        ),

        "node_count": len(nodes),

        "connection_count": connection_count,

        "branch_count": branch_count,

        # -------------------------------------------------
        # TRIGGERS
        # -------------------------------------------------

        "trigger_count": len(
            trigger_nodes
        ),

        "trigger_nodes": [
            _node_name(node)
            for node in trigger_nodes
        ],

        # -------------------------------------------------
        # AI
        # -------------------------------------------------

        "ai_node_count": len(
            ai_nodes
        ),

        "ai_nodes": [
            _node_name(node)
            for node in ai_nodes
        ],

        # -------------------------------------------------
        # INTEGRATIONS
        # -------------------------------------------------

        "integration_count": len(
            integration_nodes
        ),

        "integration_nodes": [
            _node_name(node)
            for node in integration_nodes
        ],

        # -------------------------------------------------
        # ERROR / RETRY
        # -------------------------------------------------

        "error_or_retry_count": len(
            error_nodes
        ),

        "error_or_retry_nodes": [
            _node_name(node)
            for node in error_nodes
        ],

        # -------------------------------------------------
        # HUMAN APPROVAL
        # -------------------------------------------------

        "approval_count": len(
            approval_nodes
        ),

        "approval_nodes": [
            _node_name(node)
            for node in approval_nodes
        ],

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        "validation_count": len(
            validation_nodes
        ),

        "validation_nodes": [
            _node_name(node)
            for node in validation_nodes
        ],

        # -------------------------------------------------
        # WEBHOOK
        # -------------------------------------------------

        "webhook_count": len(
            webhook_nodes
        ),

        "webhook_nodes": [
            _node_name(node)
            for node in webhook_nodes
        ],

        # -------------------------------------------------
        # TIMEOUT
        # -------------------------------------------------

        "timeout_count": len(
            timeout_nodes
        ),

        "timeout_nodes": [
            _node_name(node)
            for node in timeout_nodes
        ],

        # -------------------------------------------------
        # CREDENTIALS
        # -------------------------------------------------

        "credential_count": len(
            credential_nodes
        ),

        "credential_nodes": [
            _node_name(node)
            for node in credential_nodes
        ],

        # -------------------------------------------------
        # OBSERVABILITY
        # -------------------------------------------------

        "logging_count": len(
            logging_nodes
        ),

        "logging_nodes": [
            _node_name(node)
            for node in logging_nodes
        ],

        # -------------------------------------------------
        # NODE TYPES
        # -------------------------------------------------

        "node_types": sorted(
            {
                str(
                    node.get(
                        "type",
                        "",
                    )
                )
                for node in nodes
                if node.get("type")
            }
        ),
    }

    return summary