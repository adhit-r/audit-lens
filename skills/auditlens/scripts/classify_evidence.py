#!/usr/bin/env python3
"""
Evidence Classification Engine for AuditLens Skill

Scans a directory of documents, extracts text content, and classifies
each document by compliance control domains. Outputs a structured
evidence catalog JSON.

Usage:
    python3 classify_evidence.py --input-dir /path/to/docs --framework iso27001 --output catalog.json
"""

import argparse
import json
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# --- Document type detection keywords ---
DOC_TYPE_KEYWORDS = {
    "Policy": ["policy", "policies", "governance", "shall", "must comply", "effective date", "approved by"],
    "Procedure": ["procedure", "step-by-step", "workflow", "how to", "instructions", "sop", "standard operating"],
    "Standard": ["standard", "baseline", "minimum requirements", "configuration standard"],
    "Guideline": ["guideline", "recommendation", "best practice", "should consider"],
    "Record": ["log", "record", "register", "inventory", "list of", "roster"],
    "Evidence Artifact": ["screenshot", "export", "configuration", "scan result", "report generated"],
    "Training Material": ["training", "awareness", "course", "module", "quiz", "certification"],
    "Risk Assessment": ["risk assessment", "risk register", "risk matrix", "threat", "likelihood", "impact"],
    "Vendor Agreement": ["vendor", "third party", "supplier", "contract", "sla", "service level", "dpa"],
}

# --- ISO 27001 control domain keywords ---
ISO27001_DOMAINS = {
    "A.5": {
        "name": "Organizational Controls",
        "keywords": ["policy", "governance", "roles", "responsibilities", "management", "risk", "asset",
                     "classification", "access control", "supplier", "incident", "business continuity",
                     "compliance", "legal", "privacy", "audit", "threat intelligence"]
    },
    "A.6": {
        "name": "People Controls",
        "keywords": ["screening", "background check", "employment", "awareness", "training",
                     "disciplinary", "termination", "nda", "confidentiality", "remote work"]
    },
    "A.7": {
        "name": "Physical Controls",
        "keywords": ["physical", "perimeter", "entry", "cctv", "surveillance", "clear desk",
                     "equipment", "cabling", "maintenance", "disposal", "media", "utilities"]
    },
    "A.8": {
        "name": "Technological Controls",
        "keywords": ["endpoint", "privileged", "authentication", "mfa", "encryption", "malware",
                     "vulnerability", "patch", "configuration", "backup", "logging", "monitoring",
                     "network", "firewall", "dlp", "development", "sdlc", "secure coding", "change management"]
    }
}

# --- SOC 2 criteria domain keywords ---
SOC2_DOMAINS = {
    "CC1": {"name": "Control Environment", "keywords": ["ethics", "integrity", "board", "governance", "organizational structure", "competence", "accountability"]},
    "CC2": {"name": "Communication and Information", "keywords": ["communication", "reporting", "internal", "external", "quality information"]},
    "CC3": {"name": "Risk Assessment", "keywords": ["risk", "assessment", "fraud", "change", "objectives"]},
    "CC4": {"name": "Monitoring", "keywords": ["monitoring", "evaluation", "deficiency", "audit", "internal audit"]},
    "CC5": {"name": "Control Activities", "keywords": ["control activities", "policies", "procedures", "technology controls"]},
    "CC6": {"name": "Logical and Physical Access", "keywords": ["access", "authentication", "authorization", "credentials", "firewall", "network", "malware", "dlp"]},
    "CC7": {"name": "System Operations", "keywords": ["configuration", "monitoring", "anomaly", "incident", "vulnerability", "remediation"]},
    "CC8": {"name": "Change Management", "keywords": ["change management", "change control", "testing", "approval", "deployment"]},
    "CC9": {"name": "Risk Mitigation", "keywords": ["vendor", "third party", "supplier", "partner", "risk mitigation"]},
    "A1": {"name": "Availability", "keywords": ["availability", "capacity", "recovery", "disaster", "business continuity", "backup", "redundancy"]},
    "PI1": {"name": "Processing Integrity", "keywords": ["processing", "validation", "accuracy", "completeness", "data quality"]},
    "C1": {"name": "Confidentiality", "keywords": ["confidential", "classification", "disposal", "sensitive"]},
    "P1-P8": {"name": "Privacy", "keywords": ["privacy", "personal", "pii", "consent", "notice", "retention", "gdpr", "data subject"]},
}

FRAMEWORK_DOMAINS = {
    "iso27001": ISO27001_DOMAINS,
    "soc2": SOC2_DOMAINS,
}


def extract_text_from_file(filepath: str) -> str:
    """Extract text content from various file formats."""
    ext = Path(filepath).suffix.lower()
    text = ""

    try:
        if ext in ['.txt', '.md', '.csv', '.log', '.json', '.yml', '.yaml']:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()

        elif ext == '.pdf':
            try:
                from pypdf import PdfReader
                reader = PdfReader(filepath)
                for page in reader.pages[:20]:  # Cap at 20 pages for speed
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except ImportError:
                import subprocess
                result = subprocess.run(['pdftotext', filepath, '-'], capture_output=True, text=True, timeout=30)
                text = result.stdout

        elif ext == '.docx':
            import subprocess
            result = subprocess.run(['pandoc', filepath, '-t', 'plain'], capture_output=True, text=True, timeout=30)
            text = result.stdout

        elif ext in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                df = pd.read_excel(filepath, nrows=100)
                text = df.to_string()
            except Exception:
                text = f"[Excel file: {os.path.basename(filepath)}]"

        elif ext in ['.html', '.htm']:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read()
            text = re.sub(r'<[^>]+>', ' ', raw)

    except Exception as e:
        text = f"[Error reading {filepath}: {str(e)}]"

    return text[:50000]  # Cap at 50k chars per doc


def detect_doc_type(text: str, filename: str) -> str:
    """Classify document type based on content and filename."""
    text_lower = text.lower()
    fn_lower = filename.lower()

    scores = {}
    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower or kw in fn_lower)
        if score > 0:
            scores[doc_type] = score

    if scores:
        return max(scores, key=scores.get)
    return "Unknown"


def map_to_controls(text: str, filename: str, framework: str) -> list:
    """Map document content to compliance control domains."""
    domains = FRAMEWORK_DOMAINS.get(framework, ISO27001_DOMAINS)
    text_lower = text.lower()
    fn_lower = filename.lower()

    mappings = []
    for domain_id, domain_info in domains.items():
        keyword_hits = sum(1 for kw in domain_info["keywords"] if kw in text_lower or kw in fn_lower)
        if keyword_hits >= 3:
            strength = "direct"
        elif keyword_hits >= 1:
            strength = "indirect"
        else:
            continue

        mappings.append({
            "domain_id": domain_id,
            "domain_name": domain_info["name"],
            "strength": strength,
            "keyword_hits": keyword_hits
        })

    return sorted(mappings, key=lambda x: x["keyword_hits"], reverse=True)


def extract_date(text: str, filename: str) -> str | None:
    """Try to extract a document date from content."""
    patterns = [
        r'(?:effective|updated|revised|dated?|version)\s*(?:date)?[\s:]*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})',
        r'(\d{4}[/\-]\d{1,2}[/\-]\d{1,2})',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    # Try filename date
    fn_match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', filename)
    if fn_match:
        return fn_match.group(1)

    return None


def assess_freshness(date_str: str | None) -> str:
    """Determine if evidence is current, aging, or stale."""
    if not date_str:
        return "unknown"

    try:
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%m-%d-%Y']:
            try:
                doc_date = datetime.strptime(date_str.strip(), fmt)
                days_old = (datetime.now() - doc_date).days
                if days_old <= 365:
                    return "current"
                elif days_old <= 730:
                    return "aging"
                else:
                    return "stale"
            except ValueError:
                continue
    except Exception:
        pass

    return "unknown"


def generate_summary(text: str, max_len: int = 200) -> str:
    """Generate a brief summary from document text."""
    # Take first meaningful paragraph
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
    if paragraphs:
        summary = paragraphs[0][:max_len]
        if len(paragraphs[0]) > max_len:
            summary = summary.rsplit(' ', 1)[0] + '...'
        return summary
    return text[:max_len].strip() + '...' if len(text) > max_len else text.strip()


def scan_directory(input_dir: str, framework: str) -> dict:
    """Main scanning function — walk directory and classify everything."""
    catalog = {
        "framework": framework.upper(),
        "scan_date": datetime.now().strftime("%Y-%m-%d"),
        "documents": [],
        "unmapped_documents": [],
        "statistics": {}
    }

    supported_extensions = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.txt', '.md',
                           '.json', '.yml', '.yaml', '.html', '.htm', '.log'}

    file_count = 0
    mapped_count = 0
    stale_count = 0

    for root, dirs, files in os.walk(input_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for fname in sorted(files):
            if Path(fname).suffix.lower() not in supported_extensions:
                continue
            if fname.startswith('.'):
                continue

            filepath = os.path.join(root, fname)
            file_count += 1

            text = extract_text_from_file(filepath)
            if not text or len(text.strip()) < 20:
                catalog["unmapped_documents"].append({
                    "filename": fname,
                    "path": filepath,
                    "reason": "Could not extract meaningful text"
                })
                continue

            doc_type = detect_doc_type(text, fname)
            mappings = map_to_controls(text, fname, framework)
            date_str = extract_date(text, fname)
            freshness = assess_freshness(date_str)

            if freshness == "stale":
                stale_count += 1

            doc_entry = {
                "filename": fname,
                "path": os.path.relpath(filepath, input_dir),
                "doc_type": doc_type,
                "control_mappings": mappings,
                "last_updated": date_str,
                "freshness": freshness,
                "summary": generate_summary(text),
                "word_count": len(text.split())
            }

            if mappings:
                catalog["documents"].append(doc_entry)
                mapped_count += 1
            else:
                catalog["unmapped_documents"].append({
                    "filename": fname,
                    "path": os.path.relpath(filepath, input_dir),
                    "reason": "No control domain mappings found"
                })

    # Compute coverage
    domains = FRAMEWORK_DOMAINS.get(framework, ISO27001_DOMAINS)
    evidenced_domains = set()
    for doc in catalog["documents"]:
        for mapping in doc["control_mappings"]:
            if mapping["strength"] == "direct":
                evidenced_domains.add(mapping["domain_id"])

    total_domains = len(domains)
    coverage_pct = (len(evidenced_domains) / total_domains * 100) if total_domains > 0 else 0

    catalog["statistics"] = {
        "total_files_scanned": file_count,
        "mapped_documents": mapped_count,
        "unmapped_documents": len(catalog["unmapped_documents"]),
        "total_control_domains": total_domains,
        "evidenced_domains": len(evidenced_domains),
        "coverage_pct": round(coverage_pct, 1),
        "stale_documents": stale_count,
        "missing_domains": [
            {"domain_id": d_id, "domain_name": d_info["name"]}
            for d_id, d_info in domains.items()
            if d_id not in evidenced_domains
        ]
    }

    return catalog


def main():
    parser = argparse.ArgumentParser(description="Classify evidence documents against compliance frameworks")
    parser.add_argument("--input-dir", required=True, help="Directory containing evidence documents")
    parser.add_argument("--framework", default="iso27001", choices=["iso27001", "soc2"],
                        help="Target compliance framework")
    parser.add_argument("--output", default="evidence_catalog.json", help="Output JSON file path")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: {args.input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {args.input_dir} against {args.framework}...")
    catalog = scan_directory(args.input_dir, args.framework)

    with open(args.output, 'w') as f:
        json.dump(catalog, f, indent=2)

    print(f"\nScan complete:")
    print(f"  Files scanned: {catalog['statistics']['total_files_scanned']}")
    print(f"  Mapped to controls: {catalog['statistics']['mapped_documents']}")
    print(f"  Unmapped: {catalog['statistics']['unmapped_documents']}")
    print(f"  Domain coverage: {catalog['statistics']['coverage_pct']}%")
    print(f"  Stale documents: {catalog['statistics']['stale_documents']}")
    print(f"\nOutput written to: {args.output}")


if __name__ == "__main__":
    main()
