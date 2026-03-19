#!/usr/bin/env python3
"""
Evidence Provenance Chain Tracker

Builds and maintains a complete lifecycle record for each compliance
evidence artifact — who created it, who reviewed/approved it, version
history, storage locations, and control mappings.

Integrates with:
  - gws CLI (Google Drive file metadata, revision history)
  - m365 CLI (SharePoint/OneDrive file metadata, version history)
  - Local filesystem (stat, git log)

Usage:
    # Build provenance from Google Drive
    python3 evidence_provenance.py --source gdrive --folder-id FOLDER_ID --output provenance.json

    # Build provenance from local files
    python3 evidence_provenance.py --source local --path /path/to/evidence --output provenance.json

    # Enrich an existing evidence catalog with provenance data
    python3 evidence_provenance.py --enrich evidence_catalog.json --output enriched_catalog.json

    # Generate a provenance report
    python3 evidence_provenance.py --report provenance.json --output provenance_report.md
"""

import argparse, json, os, re, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path


def run_cmd(cmd, timeout=30):
    """Run a shell command and return stdout as string."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() if r.returncode == 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None


def check_tool(name):
    """Check if a CLI tool is available."""
    return run_cmd(f"command -v {name}") is not None


# ============================================================
# Google Drive provenance via gws CLI
# ============================================================
def gdrive_list_files(folder_id):
    """List files in a Google Drive folder with metadata."""
    cmd = f'''gws drive files list --params '{{"q": "\\"{folder_id}\\" in parents", "fields": "files(id,name,mimeType,modifiedTime,createdTime,owners,lastModifyingUser,version,permissions)"}}\' --page-all'''
    result = run_cmd(cmd, timeout=60)
    if not result:
        return []
    try:
        data = json.loads(result)
        return data.get("files", [])
    except json.JSONDecodeError:
        return []


def gdrive_get_revisions(file_id):
    """Get revision history for a Google Drive file."""
    cmd = f'''gws drive revisions list --params '{{"fileId": "{file_id}", "fields": "revisions(id,modifiedTime,lastModifyingUser,size)"}}\''''
    result = run_cmd(cmd, timeout=30)
    if not result:
        return []
    try:
        data = json.loads(result)
        return data.get("revisions", [])
    except json.JSONDecodeError:
        return []


def build_gdrive_provenance(folder_id):
    """Build provenance records from Google Drive folder."""
    files = gdrive_list_files(folder_id)
    records = []

    for f in files:
        revisions = gdrive_get_revisions(f["id"])

        owners = f.get("owners", [])
        owner_email = owners[0].get("emailAddress", "unknown") if owners else "unknown"

        last_modifier = f.get("lastModifyingUser", {})
        last_modifier_email = last_modifier.get("emailAddress", "unknown")

        version_history = []
        for rev in revisions:
            rev_user = rev.get("lastModifyingUser", {})
            version_history.append({
                "revision_id": rev.get("id"),
                "date": rev.get("modifiedTime"),
                "modified_by": rev_user.get("emailAddress", "unknown"),
                "size_bytes": rev.get("size"),
            })

        # Extract permissions for access tracking
        permissions = []
        for perm in f.get("permissions", []):
            permissions.append({
                "role": perm.get("role"),
                "type": perm.get("type"),
                "email": perm.get("emailAddress"),
            })

        record = {
            "evidence_id": f"EVD-GD-{f['id'][:8]}",
            "filename": f.get("name"),
            "source": "google_drive",
            "file_id": f["id"],
            "mime_type": f.get("mimeType"),
            "created_by": owner_email,
            "created_date": f.get("createdTime"),
            "last_modified_by": last_modifier_email,
            "last_modified_date": f.get("modifiedTime"),
            "current_version": f.get("version"),
            "version_count": len(version_history),
            "version_history": version_history[-10:],  # Last 10 revisions
            "storage_locations": [f"Google Drive: file_id={f['id']}"],
            "access_permissions": permissions,
            "reviewed_by": None,  # Requires manual input or metadata extraction
            "review_date": None,
            "approved_by": None,
            "approved_date": None,
            "provenance_confidence": "high",  # GDrive metadata is authoritative
        }
        records.append(record)

    return records


# ============================================================
# Microsoft 365 provenance via m365 CLI
# ============================================================
def m365_list_files(site_url, folder):
    """List files in a SharePoint document library."""
    cmd = f'm365 spo file list --webUrl "{site_url}" --folder "{folder}" --output json'
    result = run_cmd(cmd, timeout=60)
    if not result:
        return []
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return []


def build_m365_provenance(site_url, folder):
    """Build provenance records from SharePoint/OneDrive."""
    files = m365_list_files(site_url, folder)
    records = []

    for f in files:
        record = {
            "evidence_id": f"EVD-SP-{f.get('UniqueId', '?')[:8]}",
            "filename": f.get("Name"),
            "source": "sharepoint",
            "file_url": f.get("ServerRelativeUrl"),
            "created_by": f.get("Author", {}).get("Email", "unknown"),
            "created_date": f.get("TimeCreated"),
            "last_modified_by": f.get("ModifiedBy", {}).get("Email", "unknown"),
            "last_modified_date": f.get("TimeLastModified"),
            "current_version": f.get("MajorVersion"),
            "version_count": f.get("Versions", 0),
            "version_history": [],
            "storage_locations": [f"SharePoint: {site_url}{f.get('ServerRelativeUrl', '')}"],
            "access_permissions": [],
            "reviewed_by": None,
            "review_date": None,
            "approved_by": None,
            "approved_date": None,
            "provenance_confidence": "high",
        }
        records.append(record)

    return records


# ============================================================
# Local filesystem provenance
# ============================================================
def build_local_provenance(path):
    """Build provenance records from local filesystem."""
    records = []
    supported = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.txt', '.md', '.json'}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in sorted(files):
            if Path(fname).suffix.lower() not in supported:
                continue
            fpath = os.path.join(root, fname)
            stat = os.stat(fpath)

            # Try git log for history
            git_log = None
            git_cmd = f'git -C "{os.path.dirname(fpath)}" log --format="%H|%an|%ae|%aI|%s" -10 -- "{fname}" 2>/dev/null'
            git_result = run_cmd(git_cmd)
            if git_result:
                git_log = []
                for line in git_result.strip().split('\n'):
                    parts = line.split('|', 4)
                    if len(parts) == 5:
                        git_log.append({
                            "commit": parts[0][:8],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4],
                        })

            record = {
                "evidence_id": f"EVD-FS-{abs(hash(fpath)) % 100000000:08d}",
                "filename": fname,
                "source": "local_filesystem",
                "file_path": os.path.relpath(fpath, path),
                "size_bytes": stat.st_size,
                "created_date": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "last_modified_date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created_by": None,  # OS doesn't reliably track this
                "last_modified_by": None,
                "current_version": None,
                "version_count": len(git_log) if git_log else None,
                "version_history": git_log or [],
                "storage_locations": [f"Local: {os.path.relpath(fpath, path)}"],
                "access_permissions": [],
                "reviewed_by": None,
                "review_date": None,
                "approved_by": None,
                "approved_date": None,
                "provenance_confidence": "medium" if git_log else "low",
            }

            # Try to extract approval/review info from document content
            extracted = extract_approval_from_content(fpath)
            if extracted:
                record.update(extracted)

            records.append(record)

    return records


def extract_approval_from_content(fpath):
    """Try to extract approval metadata from document text."""
    ext = Path(fpath).suffix.lower()
    text = ""

    try:
        if ext in ('.txt', '.md', '.csv'):
            with open(fpath, 'r', errors='replace') as f:
                text = f.read()[:5000]
        elif ext == '.pdf':
            r = subprocess.run(['pdftotext', '-l', '2', fpath, '-'],
                             capture_output=True, text=True, timeout=10)
            text = r.stdout[:5000] if r.returncode == 0 else ""
        elif ext == '.docx':
            r = subprocess.run(['pandoc', fpath, '-t', 'plain'],
                             capture_output=True, text=True, timeout=10)
            text = r.stdout[:5000] if r.returncode == 0 else ""
    except Exception:
        return None

    if not text:
        return None

    result = {}

    # Look for approval patterns
    approval_patterns = [
        r"(?:approved by|approver)[:\s]*([A-Za-z\s\.]+?)(?:\s*(?:on|date)[:\s]*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}))?",
        r"(?:signed|authorized by)[:\s]*([A-Za-z\s\.]+?)(?:\s*(?:on|date)[:\s]*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}))?",
    ]
    for p in approval_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            result["approved_by"] = m.group(1).strip()[:50]
            if m.group(2):
                result["approved_date"] = m.group(2)
            break

    # Look for review patterns
    review_patterns = [
        r"(?:reviewed by|reviewer)[:\s]*([A-Za-z\s\.]+?)(?:\s*(?:on|date)[:\s]*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}))?",
        r"(?:last review|review date)[:\s]*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
    ]
    for p in review_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            if m.lastindex and m.lastindex >= 2:
                result["reviewed_by"] = m.group(1).strip()[:50]
                result["review_date"] = m.group(2)
            elif m.lastindex == 1:
                result["review_date"] = m.group(1)
            break

    # Look for version info
    version_pattern = r"(?:version|rev)[:\s]*(\d+[\.\d]*)"
    m = re.search(version_pattern, text, re.IGNORECASE)
    if m:
        result["document_version"] = m.group(1)

    return result if result else None


# ============================================================
# Enrich existing catalog with provenance
# ============================================================
def enrich_catalog(catalog_path, provenance_records):
    """Add provenance data to an existing evidence catalog."""
    with open(catalog_path) as f:
        catalog = json.load(f)

    # Build lookup by filename
    prov_by_name = {}
    for rec in provenance_records:
        prov_by_name[rec["filename"].lower()] = rec

    enriched = 0
    for doc in catalog.get("documents", []):
        fname = doc.get("filename", "").lower()
        if fname in prov_by_name:
            doc["provenance"] = prov_by_name[fname]
            enriched += 1

    catalog["provenance_enrichment"] = {
        "enriched_date": datetime.now().isoformat(),
        "documents_enriched": enriched,
        "total_documents": len(catalog.get("documents", [])),
    }

    return catalog


# ============================================================
# Report generation
# ============================================================
def generate_provenance_report(provenance_records):
    """Generate a markdown provenance report."""
    lines = []
    lines.append("# Evidence Provenance Report")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total evidence artifacts: {len(provenance_records)}\n")

    # Summary stats
    high_conf = sum(1 for r in provenance_records if r.get("provenance_confidence") == "high")
    med_conf = sum(1 for r in provenance_records if r.get("provenance_confidence") == "medium")
    low_conf = sum(1 for r in provenance_records if r.get("provenance_confidence") == "low")
    with_approval = sum(1 for r in provenance_records if r.get("approved_by"))
    with_review = sum(1 for r in provenance_records if r.get("reviewed_by") or r.get("review_date"))

    lines.append("## Provenance Quality Summary\n")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| High confidence provenance | {high_conf} |")
    lines.append(f"| Medium confidence | {med_conf} |")
    lines.append(f"| Low confidence | {low_conf} |")
    lines.append(f"| Has approval record | {with_approval} |")
    lines.append(f"| Has review record | {with_review} |")

    # Provenance gaps (items without full lifecycle)
    lines.append("\n## Provenance Gaps\n")
    lines.append("Documents missing lifecycle metadata:\n")
    for r in provenance_records:
        gaps = []
        if not r.get("approved_by"):
            gaps.append("no approver")
        if not r.get("reviewed_by") and not r.get("review_date"):
            gaps.append("no review record")
        if not r.get("version_history") or len(r.get("version_history", [])) == 0:
            gaps.append("no version history")
        if gaps:
            lines.append(f"- **{r['filename']}**: {', '.join(gaps)}")

    # Full inventory
    lines.append("\n## Full Evidence Inventory\n")
    for r in provenance_records:
        lines.append(f"### {r.get('evidence_id', '?')} — {r['filename']}\n")
        lines.append(f"- **Source**: {r.get('source', '?')}")
        lines.append(f"- **Created**: {r.get('created_date', '?')} by {r.get('created_by', '?')}")
        lines.append(f"- **Last Modified**: {r.get('last_modified_date', '?')} by {r.get('last_modified_by', '?')}")
        if r.get("approved_by"):
            lines.append(f"- **Approved**: {r['approved_date'] or '?'} by {r['approved_by']}")
        if r.get("reviewed_by"):
            lines.append(f"- **Reviewed**: {r.get('review_date', '?')} by {r['reviewed_by']}")
        lines.append(f"- **Version**: {r.get('current_version', '?')} ({r.get('version_count', '?')} revisions)")
        lines.append(f"- **Confidence**: {r.get('provenance_confidence', '?')}")
        lines.append(f"- **Locations**: {', '.join(r.get('storage_locations', []))}")
        lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Evidence Provenance Chain Tracker")
    p.add_argument("--source", choices=["gdrive", "m365", "local"],
                   help="Evidence source to scan")
    p.add_argument("--folder-id", help="Google Drive folder ID")
    p.add_argument("--site-url", help="SharePoint site URL")
    p.add_argument("--folder", help="SharePoint folder path")
    p.add_argument("--path", help="Local filesystem path")
    p.add_argument("--enrich", help="Enrich existing evidence_catalog.json")
    p.add_argument("--report", help="Generate report from provenance.json")
    p.add_argument("--output", default="provenance.json", help="Output file")
    args = p.parse_args()

    if args.report:
        with open(args.report) as f:
            records = json.load(f)
        report = generate_provenance_report(records)
        if args.output.endswith('.md'):
            with open(args.output, 'w') as f:
                f.write(report)
        else:
            print(report)
        print(f"Report written to {args.output}", file=sys.stderr)
        return

    records = []
    if args.source == "gdrive":
        if not args.folder_id:
            print("--folder-id required for gdrive source", file=sys.stderr)
            sys.exit(1)
        if not check_tool("gws"):
            print("gws CLI not found. Install: npm i -g @googleworkspace/cli", file=sys.stderr)
            sys.exit(1)
        records = build_gdrive_provenance(args.folder_id)

    elif args.source == "m365":
        if not args.site_url or not args.folder:
            print("--site-url and --folder required for m365 source", file=sys.stderr)
            sys.exit(1)
        if not check_tool("m365"):
            print("m365 CLI not found. Install: npm i -g @pnp/cli-microsoft365", file=sys.stderr)
            sys.exit(1)
        records = build_m365_provenance(args.site_url, args.folder)

    elif args.source == "local":
        if not args.path:
            print("--path required for local source", file=sys.stderr)
            sys.exit(1)
        records = build_local_provenance(args.path)

    if args.enrich:
        enriched = enrich_catalog(args.enrich, records)
        with open(args.output, 'w') as f:
            json.dump(enriched, f, indent=2)
        e = enriched.get("provenance_enrichment", {})
        print(f"Enriched {e.get('documents_enriched', 0)}/{e.get('total_documents', 0)} documents", file=sys.stderr)
    else:
        with open(args.output, 'w') as f:
            json.dump(records, f, indent=2)
        print(f"Built {len(records)} provenance records → {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
