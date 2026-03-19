#!/usr/bin/env python3
"""
AuditLens MCP Server
This script wraps the core AuditLens logic as Model Context Protocol (MCP) tools.
"""

import os
import sys
import json
import subprocess
from typing import List, Optional

# --- MCP Protocol Essentials ---

def send_response(result: dict):
    print(json.dumps(result))
    sys.stdout.flush()

def log_error(message: str):
    print(json.dumps({"error": message}), file=sys.stderr)
    sys.stderr.flush()

# --- AuditLens Tool Wrappers ---

def classify_evidence(directory: str):
    """Classifies documents in a directory."""
    script_path = os.path.join(os.path.dirname(__file__), "classify_evidence.py")
    try:
        result = subprocess.check_output([sys.executable, script_path, directory], text=True)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def audit_query(query: str, catalog_path: Optional[str] = None):
    """Runs a natural language audit query."""
    script_path = os.path.join(os.path.dirname(__file__), "audit_query_engine.py")
    args = [sys.executable, script_path, query]
    if catalog_path:
        args.extend(["--catalog", catalog_path])
    try:
        result = subprocess.check_output(args, text=True)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def track_provenance(directory: str):
    """Tracks evidence provenance."""
    script_path = os.path.join(os.path.dirname(__file__), "evidence_provenance.py")
    try:
        result = subprocess.check_output([sys.executable, script_path, directory], text=True)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def score_vendor(questionnaire_path: str):
    """Scores a vendor security questionnaire."""
    script_path = os.path.join(os.path.dirname(__file__), "vendor_scorer.py")
    try:
        result = subprocess.check_output([sys.executable, script_path, questionnaire_path], text=True)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

def draft_remediation(domain_id: str, framework: str = "iso27001"):
    """Drafts baseline compliance policy templates."""
    script_path = os.path.join(os.path.dirname(__file__), "draft_remediation.py")
    try:
        result = subprocess.check_output([sys.executable, script_path, domain_id, "--framework", framework], text=True)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e)}

# --- Manifest ---

TOOLS = [
    {
        "name": "classify_evidence",
        "description": "Classifies documents by type and maps them to compliance control domains.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Path to the directory containing evidence documents."}
            },
            "required": ["directory"]
        }
    },
    {
        "name": "audit_query",
        "description": "Powerful natural language query engine for auditing the evidence catalog.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The auditor's question (e.g., 'Do we have encryption policies?')"},
                "catalog_path": {"type": "string", "description": "Optional path to a pre-generated evidence catalog (JSON)."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "track_provenance",
        "description": "Tracks the lifecycle and history of compliance evidence artifacts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Path to the directory to scan for provenance."}
            },
            "required": ["directory"]
        }
    },
    {
        "name": "score_vendor",
        "description": "Automates the scoring of vendor security questionnaires (SIG/CAIQ).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "questionnaire_path": {"type": "string", "description": "Path to the vendor questionnaire (CSV)."}
            },
            "required": ["questionnaire_path"]
        }
    },
    {
        "name": "draft_remediation",
        "description": "Auto-generates baseline compliance policy drafts to speed up gap remediation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain_id": {"type": "string", "description": "The control domain ID missing evidence (e.g., A.5, CC6)."},
                "framework": {"type": "string", "description": "The target framework (iso27001, soc2). Defaults to iso27001."}
            },
            "required": ["domain_id"]
        }
    }
]

# --- Main Logic ---

def main():
    if len(sys.argv) < 2:
        # Show manifest (for MCP registration)
        print(json.dumps({"name": "auditlens", "version": "1.0.0", "tools": TOOLS}, indent=2))
        return

    # Handle tool calls (simple JSON-RPC style for demonstration)
    try:
        call = json.loads(sys.argv[1])
        tool_name = call.get("name")
        arguments = call.get("arguments", {})

        if tool_name == "classify_evidence":
            send_response(classify_evidence(arguments["directory"]))
        elif tool_name == "audit_query":
            send_response(audit_query(arguments["query"], arguments.get("catalog_path")))
        elif tool_name == "track_provenance":
            send_response(track_provenance(arguments["directory"]))
        elif tool_name == "score_vendor":
            send_response(score_vendor(arguments["questionnaire_path"]))
        elif tool_name == "draft_remediation":
            send_response(draft_remediation(arguments["domain_id"], arguments.get("framework", "iso27001")))
        else:
            log_error(f"Tool {tool_name} not found.")
    except Exception as e:
        log_error(f"Internal error: {str(e)}")

if __name__ == "__main__":
    main()
