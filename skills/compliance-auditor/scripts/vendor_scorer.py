#!/usr/bin/env python3
"""
Automated Vendor Security Scorer

Ingests vendor security questionnaires (SIG Lite, CAIQ, custom CSVs),
scores vendor security posture by control domain, maps vendor controls
against the organization's framework requirements, and flags gaps.

Usage:
    # Score a vendor questionnaire CSV
    python3 vendor_scorer.py --input vendor_responses.csv --framework soc2 --output vendor_score.json

    # Compare multiple vendors
    python3 vendor_scorer.py --compare vendor1_score.json vendor2_score.json --output comparison.json

    # Generate vendor risk report
    python3 vendor_scorer.py --report vendor_score.json --output vendor_report.md
"""

import argparse, csv, json, os, re, sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict


# --- SIG Lite domain mapping ---
SIG_DOMAINS = {
    "A": {"name": "Enterprise Risk Management", "weight": 0.8, "framework_map": {"soc2": ["CC3.1-CC3.4"], "iso27001": ["A.5.7"]}},
    "B": {"name": "Security Policy", "weight": 1.0, "framework_map": {"soc2": ["CC5.3"], "iso27001": ["A.5.1"]}},
    "C": {"name": "Organizational Security", "weight": 0.9, "framework_map": {"soc2": ["CC1.3"], "iso27001": ["A.5.2"]}},
    "D": {"name": "Asset and Info Management", "weight": 0.9, "framework_map": {"soc2": ["CC6.1"], "iso27001": ["A.5.9-A.5.14"]}},
    "E": {"name": "Human Resource Security", "weight": 0.8, "framework_map": {"soc2": ["CC1.4"], "iso27001": ["A.6.1-A.6.6"]}},
    "F": {"name": "Physical and Environmental", "weight": 0.7, "framework_map": {"soc2": ["CC6.4"], "iso27001": ["A.7.1-A.7.14"]}},
    "G": {"name": "IT Operations Management", "weight": 1.0, "framework_map": {"soc2": ["CC7.1-CC7.5"], "iso27001": ["A.8.1-A.8.34"]}},
    "H": {"name": "Access Control", "weight": 1.0, "framework_map": {"soc2": ["CC6.1-CC6.4"], "iso27001": ["A.5.15-A.5.18", "A.8.2-A.8.5"]}},
    "I": {"name": "Application Security", "weight": 0.9, "framework_map": {"soc2": ["CC8.1"], "iso27001": ["A.8.25-A.8.31"]}},
    "J": {"name": "Cybersecurity Incident Mgmt", "weight": 1.0, "framework_map": {"soc2": ["CC7.3-CC7.5"], "iso27001": ["A.5.24-A.5.28"]}},
    "K": {"name": "Operational Resilience", "weight": 0.9, "framework_map": {"soc2": ["A1.1-A1.3"], "iso27001": ["A.5.29-A.5.30"]}},
    "L": {"name": "Compliance and Ops Risk", "weight": 0.8, "framework_map": {"soc2": ["CC4.1-CC4.2"], "iso27001": ["A.5.35-A.5.36"]}},
    "M": {"name": "Endpoint Device Security", "weight": 0.9, "framework_map": {"soc2": ["CC6.8"], "iso27001": ["A.8.1", "A.8.7"]}},
    "N": {"name": "Network Security", "weight": 1.0, "framework_map": {"soc2": ["CC6.5-CC6.6"], "iso27001": ["A.8.20-A.8.22"]}},
    "O": {"name": "Privacy", "weight": 0.9, "framework_map": {"soc2": ["P1.1-P8.1"], "iso27001": ["A.5.34"]}},
    "P": {"name": "Threat Management", "weight": 0.9, "framework_map": {"soc2": ["CC7.2"], "iso27001": ["A.8.7-A.8.8", "A.8.16"]}},
    "Q": {"name": "Server Security", "weight": 0.9, "framework_map": {"soc2": ["CC7.1"], "iso27001": ["A.8.9"]}},
    "R": {"name": "Cloud Hosting Services", "weight": 1.0, "framework_map": {"soc2": ["CC6.1", "CC6.7"], "iso27001": ["A.5.23"]}},
}

# --- Response scoring rules ---
POSITIVE_RESPONSES = {"yes", "y", "implemented", "in place", "compliant", "true", "1", "full", "complete", "operational"}
PARTIAL_RESPONSES = {"partial", "partially", "in progress", "planned", "developing", "some", "0.5"}
NEGATIVE_RESPONSES = {"no", "n", "not implemented", "not in place", "non-compliant", "false", "0", "none", "n/a"}
COMPENSATING_RESPONSES = {"compensating", "alternative", "mitigated", "workaround"}


def score_response(response: str) -> tuple[float, str]:
    """Score a single questionnaire response. Returns (score, classification)."""
    if not response:
        return 0.0, "no_response"

    resp = response.strip().lower()

    if resp in POSITIVE_RESPONSES or resp.startswith("yes"):
        return 1.0, "implemented"
    elif resp in PARTIAL_RESPONSES or "partial" in resp or "progress" in resp:
        return 0.5, "partial"
    elif resp in COMPENSATING_RESPONSES or "compensat" in resp:
        return 0.7, "compensating"
    elif resp in NEGATIVE_RESPONSES or resp.startswith("no") or resp == "n/a":
        return 0.0, "not_implemented"
    elif len(resp) > 20:
        # Long text response — likely a description. Score based on content quality
        quality_indicators = ["policy", "procedure", "annually", "quarterly", "encrypted",
                            "monitored", "reviewed", "automated", "documented", "trained"]
        hits = sum(1 for kw in quality_indicators if kw in resp)
        if hits >= 3:
            return 0.9, "detailed_yes"
        elif hits >= 1:
            return 0.6, "partial_detail"
        else:
            return 0.3, "vague_response"
    else:
        return 0.3, "unclear"


def detect_questionnaire_format(headers: list[str]) -> str:
    """Detect questionnaire format from CSV headers."""
    h_lower = [h.lower() for h in headers]

    if any("sig" in h for h in h_lower) or any("shared assessment" in h for h in h_lower):
        return "sig"
    elif any("caiq" in h for h in h_lower) or any("consensus" in h for h in h_lower):
        return "caiq"
    elif any("question" in h for h in h_lower) and any("response" in h or "answer" in h for h in h_lower):
        return "generic"
    else:
        return "unknown"


def find_columns(headers: list[str]) -> dict:
    """Find the question and response columns in the CSV."""
    h_lower = [h.lower() for h in headers]
    cols = {"question": None, "response": None, "domain": None, "id": None, "notes": None}

    for i, h in enumerate(h_lower):
        if not cols["question"] and any(kw in h for kw in ["question", "requirement", "control", "criteria"]):
            cols["question"] = i
        if not cols["response"] and any(kw in h for kw in ["response", "answer", "vendor response", "status"]):
            cols["response"] = i
        if not cols["domain"] and any(kw in h for kw in ["domain", "category", "section", "area"]):
            cols["domain"] = i
        if not cols["id"] and any(kw in h for kw in ["id", "ref", "number", "#"]):
            cols["id"] = i
        if not cols["notes"] and any(kw in h for kw in ["notes", "comment", "evidence", "detail"]):
            cols["notes"] = i

    # Fallback: assume first column is question, second is response
    if cols["question"] is None:
        cols["question"] = 0
    if cols["response"] is None:
        cols["response"] = min(1, len(headers) - 1)

    return cols


def infer_domain(question_text: str) -> str:
    """Infer the SIG domain from question text."""
    q = question_text.lower()

    domain_keywords = {
        "A": ["enterprise risk", "risk management program"],
        "B": ["security policy", "information security policy"],
        "C": ["organizational", "roles and responsibilities", "governance"],
        "D": ["asset", "classification", "data handling", "inventory"],
        "E": ["human resource", "background check", "screening", "training", "awareness"],
        "F": ["physical", "facility", "badge", "environmental"],
        "G": ["operations", "change management", "capacity", "backup"],
        "H": ["access control", "authentication", "password", "mfa", "privilege"],
        "I": ["application", "sdlc", "code review", "secure development"],
        "J": ["incident", "breach", "response", "forensic"],
        "K": ["business continuity", "disaster recovery", "resilience"],
        "L": ["compliance", "audit", "regulatory", "legal"],
        "M": ["endpoint", "mobile", "device", "antivirus", "edr"],
        "N": ["network", "firewall", "segmentation", "vpn", "ids"],
        "O": ["privacy", "personal data", "gdpr", "consent", "data subject"],
        "P": ["threat", "vulnerability", "penetration", "scan"],
        "Q": ["server", "hardening", "configuration", "patch"],
        "R": ["cloud", "aws", "azure", "gcp", "saas", "iaas"],
    }

    best_domain = "G"  # Default to IT Ops
    best_score = 0
    for domain, keywords in domain_keywords.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > best_score:
            best_score = score
            best_domain = domain

    return best_domain


def score_questionnaire(input_path: str, framework: str = "soc2") -> dict:
    """Score a vendor questionnaire CSV file."""
    with open(input_path, 'r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    fmt = detect_questionnaire_format(headers)
    cols = find_columns(headers)

    domain_scores = defaultdict(lambda: {"total": 0, "score": 0.0, "questions": [],
                                          "implemented": 0, "partial": 0, "not_implemented": 0, "no_response": 0})
    all_questions = []

    for row_idx, row in enumerate(rows):
        if len(row) <= max(v for v in cols.values() if v is not None):
            continue

        question = row[cols["question"]].strip() if cols["question"] is not None else ""
        response = row[cols["response"]].strip() if cols["response"] is not None else ""
        domain_raw = row[cols["domain"]].strip() if cols["domain"] is not None else ""
        q_id = row[cols["id"]].strip() if cols["id"] is not None else f"Q{row_idx+1}"

        if not question or len(question) < 5:
            continue

        # Determine domain
        domain = domain_raw[0].upper() if domain_raw and domain_raw[0].upper() in SIG_DOMAINS else infer_domain(question)

        score, classification = score_response(response)

        ds = domain_scores[domain]
        ds["total"] += 1
        ds["score"] += score
        ds[classification if classification in ds else "no_response"] += 1

        q_entry = {
            "id": q_id,
            "domain": domain,
            "question": question[:200],
            "response": response[:300],
            "score": score,
            "classification": classification,
        }
        ds["questions"].append(q_entry)
        all_questions.append(q_entry)

    # Calculate domain-level scores
    domain_results = {}
    total_weighted_score = 0
    total_weight = 0

    for domain_id, ds in domain_scores.items():
        domain_info = SIG_DOMAINS.get(domain_id, {"name": f"Domain {domain_id}", "weight": 1.0, "framework_map": {}})
        pct = (ds["score"] / ds["total"] * 100) if ds["total"] > 0 else 0
        weight = domain_info["weight"]

        total_weighted_score += pct * weight
        total_weight += weight

        domain_results[domain_id] = {
            "domain_name": domain_info["name"],
            "questions_count": ds["total"],
            "score_pct": round(pct, 1),
            "implemented": ds["implemented"],
            "partial": ds["partial"],
            "not_implemented": ds["not_implemented"],
            "no_response": ds["no_response"],
            "weight": weight,
            "framework_controls": domain_info.get("framework_map", {}).get(framework, []),
            "gaps": [q for q in ds["questions"] if q["score"] == 0],
        }

    overall_score = round(total_weighted_score / total_weight, 1) if total_weight > 0 else 0

    # Risk tiering
    if overall_score >= 85:
        risk_tier = "Low"
        risk_color = "green"
    elif overall_score >= 70:
        risk_tier = "Medium"
        risk_color = "amber"
    elif overall_score >= 50:
        risk_tier = "High"
        risk_color = "red"
    else:
        risk_tier = "Critical"
        risk_color = "red"

    return {
        "vendor_name": Path(input_path).stem.replace("_", " ").replace("-", " ").title(),
        "assessment_date": datetime.now().strftime("%Y-%m-%d"),
        "questionnaire_format": fmt,
        "framework": framework,
        "overall_score": overall_score,
        "risk_tier": risk_tier,
        "risk_color": risk_color,
        "total_questions": len(all_questions),
        "domain_scores": domain_results,
        "critical_gaps": [q for q in all_questions if q["score"] == 0][:20],
        "framework_gap_mapping": build_framework_gap_map(domain_results, framework),
    }


def build_framework_gap_map(domain_results: dict, framework: str) -> list:
    """Map vendor gaps to the organization's framework controls."""
    gap_map = []
    for domain_id, dr in domain_results.items():
        if dr["score_pct"] < 70:  # Below threshold
            for ctrl in dr.get("framework_controls", []):
                gap_map.append({
                    "vendor_domain": f"{domain_id}: {dr['domain_name']}",
                    "vendor_score": dr["score_pct"],
                    "org_control": ctrl,
                    "risk": "high" if dr["score_pct"] < 50 else "medium",
                    "recommendation": f"Vendor is weak in {dr['domain_name']}. "
                                    f"Your {ctrl} control relies on vendor coverage here. "
                                    f"Consider compensating controls or vendor remediation plan.",
                })
    return sorted(gap_map, key=lambda x: x["vendor_score"])


def compare_vendors(score_files: list[str]) -> dict:
    """Compare multiple vendor scores side by side."""
    vendors = []
    for f in score_files:
        with open(f) as fh:
            vendors.append(json.load(fh))

    comparison = {
        "comparison_date": datetime.now().strftime("%Y-%m-%d"),
        "vendors": [],
        "recommendation": None,
    }

    for v in vendors:
        comparison["vendors"].append({
            "name": v["vendor_name"],
            "overall_score": v["overall_score"],
            "risk_tier": v["risk_tier"],
            "total_questions": v["total_questions"],
            "domain_highlights": {
                did: dr["score_pct"]
                for did, dr in v.get("domain_scores", {}).items()
            },
            "critical_gap_count": len(v.get("critical_gaps", [])),
        })

    # Sort by score descending
    comparison["vendors"].sort(key=lambda x: -x["overall_score"])
    if len(comparison["vendors"]) >= 2:
        best = comparison["vendors"][0]
        comparison["recommendation"] = (
            f"{best['name']} scores highest at {best['overall_score']}% "
            f"(Risk: {best['risk_tier']}). "
            f"Consider this vendor for lower residual risk."
        )

    return comparison


def generate_vendor_report(score: dict) -> str:
    """Generate a markdown vendor risk report."""
    lines = []
    lines.append(f"# Vendor Security Assessment: {score['vendor_name']}")
    lines.append(f"\nDate: {score['assessment_date']} | Framework: {score['framework'].upper()}")
    lines.append(f"Format: {score['questionnaire_format'].upper()} | Questions: {score['total_questions']}\n")

    # Overall score
    lines.append(f"## Overall Score: {score['overall_score']}% — Risk Tier: **{score['risk_tier']}**\n")

    # Domain breakdown
    lines.append("## Domain Scores\n")
    lines.append("| Domain | Score | Implemented | Partial | Gaps | Framework Controls |")
    lines.append("|--------|-------|-------------|---------|------|-------------------|")
    for did in sorted(score.get("domain_scores", {}).keys()):
        dr = score["domain_scores"][did]
        ctrls = ", ".join(dr.get("framework_controls", []))
        lines.append(f"| {did}: {dr['domain_name']} | {dr['score_pct']}% | {dr['implemented']} | {dr['partial']} | {dr['not_implemented']} | {ctrls} |")

    # Critical gaps
    gaps = score.get("critical_gaps", [])
    if gaps:
        lines.append(f"\n## Critical Gaps ({len(gaps)} items)\n")
        for g in gaps[:15]:
            lines.append(f"- **{g['id']}** ({g['domain']}): {g['question'][:120]}")

    # Framework impact
    fw_gaps = score.get("framework_gap_mapping", [])
    if fw_gaps:
        lines.append(f"\n## Impact on Your Framework ({score['framework'].upper()})\n")
        lines.append("| Vendor Domain | Vendor Score | Your Control | Risk | Recommendation |")
        lines.append("|--------------|-------------|-------------|------|----------------|")
        for fg in fw_gaps[:10]:
            lines.append(f"| {fg['vendor_domain']} | {fg['vendor_score']}% | {fg['org_control']} | {fg['risk']} | {fg['recommendation'][:80]} |")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Vendor Security Scorer")
    p.add_argument("--input", help="Vendor questionnaire CSV file")
    p.add_argument("--framework", default="soc2", choices=["soc2", "iso27001"],
                   help="Organization's framework for gap mapping")
    p.add_argument("--compare", nargs="+", help="Compare multiple vendor_score.json files")
    p.add_argument("--report", help="Generate report from vendor_score.json")
    p.add_argument("--output", default="vendor_score.json")
    args = p.parse_args()

    if args.report:
        with open(args.report) as f:
            score = json.load(f)
        report = generate_vendor_report(score)
        if args.output.endswith('.md'):
            with open(args.output, 'w') as f:
                f.write(report)
        else:
            print(report)
        return

    if args.compare:
        result = compare_vendors(args.compare)
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Compared {len(args.compare)} vendors → {args.output}", file=sys.stderr)
        for v in result["vendors"]:
            print(f"  {v['name']}: {v['overall_score']}% ({v['risk_tier']})", file=sys.stderr)
        if result.get("recommendation"):
            print(f"\nRecommendation: {result['recommendation']}", file=sys.stderr)
        return

    if args.input:
        score = score_questionnaire(args.input, args.framework)
        with open(args.output, 'w') as f:
            json.dump(score, f, indent=2)
        print(f"\nVendor: {score['vendor_name']}", file=sys.stderr)
        print(f"Score: {score['overall_score']}%  Risk: {score['risk_tier']}", file=sys.stderr)
        print(f"Questions: {score['total_questions']}  Critical Gaps: {len(score.get('critical_gaps', []))}", file=sys.stderr)
        print(f"Output: {args.output}", file=sys.stderr)
        return

    print("Specify --input, --compare, or --report", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
