#!/usr/bin/env python3
"""
Natural Language Audit Query Engine

Lets auditors ask plain-English questions and get instant answers from
the evidence catalog. Translates queries into structured lookups.

Usage:
    python3 audit_query_engine.py --catalog evidence_catalog.json --query "When was the access review last performed?"
    python3 audit_query_engine.py --catalog evidence_catalog.json --interactive
"""

import argparse, json, sys, re
from datetime import datetime

QUERY_PATTERNS = {
    "find_evidence": [
        r"(?:show|find|list|get|what)\b.*(?:evidence|documents?|artifacts?|proof)\b.*(?:for|about|related to|regarding)\s+(.+)",
        r"(?:do we have)\b.*(?:evidence|documentation|proof)\b.*(?:for|about)\s+(.+)",
    ],
    "check_control": [
        r"(?:what is the status of|check|how are we on)\s+(?:control\s+)?([A-Z0-9\.]+)",
        r"(?:show me)\s+(?:control\s+)?([A-Z0-9\.]+)",
    ],
    "find_gaps": [
        r"(?:what|which|show|list)\b.*(?:gaps?|missing|lacking|deficien)",
        r"(?:where are we|what are our)\b.*(?:weak|vulnerable|exposed|gaps?)",
    ],
    "check_freshness": [
        r"(?:when was|last time|how old|how recent)\b.*(?:review|update|modif|chang|renew)",
        r"(?:what|which)\b.*(?:stale|expired|outdated|old|aging)",
    ],
    "find_owner": [
        r"(?:who)\b.*(?:own|responsible|approved|created|reviewed|manages?)\b.*(?:for|the)?\s*(.+)",
    ],
    "count_stats": [
        r"(?:how many|count|total|number of)\b.*(?:controls?|documents?|gaps?|policies?|evidence)",
        r"(?:summary|overview|dashboard|stats|statistics)",
    ],
    "remediation": [
        r"(?:what do we need to|how to|what should we)\b.*(?:fix|remediate|address|close|resolve)\b",
        r"(?:remediation|action items?|next steps?|to.?do|priorit)",
    ],
}

DOMAIN_KEYWORDS = {
    "access control": ["access", "authentication", "authorization", "login", "mfa", "password", "rbac", "privilege"],
    "encryption": ["encrypt", "cryptograph", "key management", "tls", "certificate"],
    "incident response": ["incident", "breach", "response", "forensic", "playbook", "siem"],
    "business continuity": ["continuity", "disaster", "recovery", "backup", "rto", "rpo"],
    "vulnerability management": ["vulnerability", "patch", "scan", "penetration", "pentest", "cve"],
    "change management": ["change management", "change control", "cab", "deployment"],
    "vendor management": ["vendor", "supplier", "third party", "outsourc", "contract", "sla"],
    "training": ["training", "awareness", "phishing", "education"],
    "physical security": ["physical", "badge", "cctv", "surveillance", "perimeter"],
    "logging": ["log", "audit trail", "monitoring", "siem", "detection"],
    "data protection": ["classification", "dlp", "data loss", "pii", "phi", "sensitive"],
    "network security": ["firewall", "network", "segmentation", "vlan", "vpn", "ids"],
    "secure development": ["sdlc", "secure coding", "code review", "sast", "dast"],
    "risk assessment": ["risk assessment", "risk register", "threat", "risk matrix"],
    "policy": ["policy", "procedure", "standard", "guideline", "governance"],
}


def load_catalog(path):
    with open(path) as f:
        return json.load(f)


def detect_intent(query):
    q = query.lower().strip()
    for intent, patterns in QUERY_PATTERNS.items():
        for p in patterns:
            m = re.search(p, q)
            if m:
                return intent, (m.group(1).strip() if m.lastindex else None)
    return "general", None


def find_domains(query):
    q = query.lower()
    hits = [(d, sum(1 for kw in kws if kw in q)) for d, kws in DOMAIN_KEYWORDS.items()]
    return [d for d, s in sorted(hits, key=lambda x: -x[1]) if s > 0]


def search_evidence(catalog, subject):
    if not subject:
        return []
    sl = subject.lower()
    scored = []
    for doc in catalog.get("documents", []):
        score = 0
        if sl in doc.get("filename", "").lower(): score += 3
        if sl in doc.get("summary", "").lower(): score += 2
        if sl in doc.get("doc_type", "").lower(): score += 1
        for m in doc.get("control_mappings", []):
            if sl in m.get("domain_name", "").lower(): score += 2
            if sl in m.get("domain_id", "").lower(): score += 3
        overlap = len(set(sl.split()) & set(doc.get("summary", "").lower().split()))
        score += overlap
        if score > 0:
            scored.append({**doc, "_score": score})
    return sorted(scored, key=lambda x: -x["_score"])[:10]


def fmt_doc(doc):
    lines = [f"  {doc.get('filename', '?')}"]
    lines.append(f"    Type: {doc.get('doc_type', '?')} | Freshness: {doc.get('freshness', '?')}")
    if doc.get("last_updated"):
        lines.append(f"    Last Updated: {doc['last_updated']}")
    lines.append(f"    Summary: {doc.get('summary', 'N/A')[:150]}")
    maps = doc.get("control_mappings", [])
    if maps:
        lines.append(f"    Controls: {', '.join(m['domain_id']+'('+m['strength']+')' for m in maps[:5])}")
    if doc.get("provenance"):
        p = doc["provenance"]
        if p.get("approved_by"):
            lines.append(f"    Approved by: {p['approved_by']} on {p.get('approved_date','?')}")
        if p.get("reviewed_by"):
            lines.append(f"    Last reviewed by: {p['reviewed_by']} on {p.get('review_date','?')}")
    return "\n".join(lines)


def process_query(catalog, query):
    intent, subject = detect_intent(query)
    domains = find_domains(query)

    if intent == "find_evidence":
        results = search_evidence(catalog, subject or " ".join(domains))
        if results:
            return f"Found {len(results)} document(s) for \"{subject or ', '.join(domains)}\":\n\n" + \
                   "\n\n".join(fmt_doc(d) for d in results)
        return f"No evidence found for \"{subject}\". This may be a gap."

    elif intent == "check_control":
        cid = subject.upper() if subject else ""
        results = search_evidence(catalog, cid)
        if results:
            return f"Control {cid} — EVIDENCED ({len(results)} documents):\n\n" + \
                   "\n\n".join(fmt_doc(d) for d in results)
        return f"Control {cid} — GAP. No evidence mapped."

    elif intent == "find_gaps":
        gaps = catalog.get("statistics", {}).get("missing_domains", [])
        if gaps:
            return f"{len(gaps)} gap(s) found:\n\n" + \
                   "\n".join(f"  {g['domain_id']}: {g['domain_name']} — MISSING" for g in gaps)
        return "No gaps — all domains have evidence."

    elif intent == "check_freshness":
        stale = [d for d in catalog.get("documents", []) if d.get("freshness") in ("stale", "aging")]
        if stale:
            return f"{len(stale)} stale/aging document(s):\n\n" + "\n\n".join(fmt_doc(d) for d in stale)
        return "All documents appear current."

    elif intent == "find_owner":
        results = search_evidence(catalog, subject)
        owned = [d for d in results if d.get("provenance")]
        if owned:
            return "\n\n".join(fmt_doc(d) for d in owned)
        if results:
            return "Found documents but no provenance/ownership data attached:\n\n" + \
                   "\n\n".join(fmt_doc(d) for d in results[:3])
        return f"No documents found matching \"{subject}\"."

    elif intent == "count_stats":
        s = catalog.get("statistics", {})
        return (f"Compliance Summary:\n"
                f"  Files scanned: {s.get('total_files_scanned', '?')}\n"
                f"  Mapped: {s.get('mapped_documents', '?')}\n"
                f"  Unmapped: {s.get('unmapped_documents', '?')}\n"
                f"  Domains evidenced: {s.get('evidenced_domains', '?')}/{s.get('total_control_domains', '?')}\n"
                f"  Coverage: {s.get('coverage_pct', '?')}%\n"
                f"  Stale: {s.get('stale_documents', '?')}")

    elif intent == "remediation":
        gaps = catalog.get("statistics", {}).get("missing_domains", [])
        stale = [d for d in catalog.get("documents", []) if d.get("freshness") == "stale"]
        out = "Remediation Priorities:\n\n"
        if gaps:
            out += f"1. CLOSE {len(gaps)} GAPS:\n" + \
                   "".join(f"   - {g['domain_id']}: {g['domain_name']}\n" for g in gaps)
        if stale:
            out += f"\n2. REFRESH {len(stale)} STALE DOCS:\n" + \
                   "".join(f"   - {d['filename']}\n" for d in stale[:5])
        return out if (gaps or stale) else "No remediation items found."

    # Fallback: semantic search
    results = search_evidence(catalog, query)
    if results:
        return f"Related documents:\n\n" + "\n\n".join(fmt_doc(d) for d in results[:5])
    if domains:
        return f"Query relates to: {', '.join(domains)}. Try: \"Show evidence for {domains[0]}\""
    return ("Try asking:\n"
            "  - \"Show me evidence for access control\"\n"
            "  - \"What gaps do we have?\"\n"
            "  - \"Which documents are stale?\"\n"
            "  - \"Give me a summary\"")


def interactive(catalog):
    print(f"{'='*55}\n  Audit Query Engine | {catalog.get('framework','?')} | {len(catalog.get('documents',[]))} docs\n{'='*55}")
    print("Ask in plain English. Type 'quit' to exit.\n")
    while True:
        try:
            q = input("auditor> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q.lower() in ("quit", "exit", "q"):
            break
        print(f"\n{process_query(catalog, q)}\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True)
    p.add_argument("--query")
    p.add_argument("--interactive", action="store_true")
    p.add_argument("--json-output", action="store_true")
    a = p.parse_args()
    cat = load_catalog(a.catalog)
    if a.interactive:
        interactive(cat)
    elif a.query:
        r = process_query(cat, a.query)
        print(json.dumps({"query": a.query, "answer": r}, indent=2) if a.json_output else r)
    else:
        print("Specify --query or --interactive", file=sys.stderr)
