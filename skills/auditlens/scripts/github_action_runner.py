#!/usr/bin/env python3
"""
AuditLens GitHub Action Runner

Executes the classify_evidence scan and formats a "Compliance Delta" 
report to be posted as a PR comment or Action Summary.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

# Add current dir to path to import classify_evidence
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from classify_evidence import scan_directory

def generate_markdown_report(catalog):
    stats = catalog['statistics']
    gaps = stats.get('missing_domains', [])
    stale = stats.get('stale_documents', 0)
    
    md = [
        "## 🛡️ AuditLens Compliance Scan",
        f"**Framework:** {catalog['framework']} | **Coverage:** {stats['coverage_pct']}%",
        "",
        "### High-Level Summary",
        f"- 📄 **Documents Scanned:** {stats['total_files_scanned']}",
        f"- 🔗 **Controls Mapped:** {stats['evidenced_domains']} / {stats['total_control_domains']}",
        f"- ⚠️ **Critical Gaps:** {len(gaps)}",
        f"- ⏳ **Stale Artifacts:** {stale}",
        ""
    ]
    
    if gaps:
        md.append("### 🚨 Critical Control Gaps Detected")
        md.append("The following domains lack sufficient documentation:")
        for g in gaps:
            md.append(f"- **{g['domain_id']}**: {g['domain_name']}")
        md.append("")
    else:
        md.append("✅ **No critical gaps detected!** All domains have evidence.")
        md.append("")
        
    md.append("*Generated automatically by [AuditLens](https://github.com/adhit-r/audit-lens).*")
    return "\n".join(md)

def post_pr_comment(repo, pr_number, token, body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = json.dumps({"body": body}).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as res:
            if res.status == 201:
                print("Successfully posted PR comment.")
    except urllib.error.URLError as e:
        print(f"Failed to post PR comment: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--framework", default="iso27001")
    args = parser.parse_args()

    # 1. Run the scan
    print(f"Running AuditLens scan on {args.input_dir}...")
    catalog = scan_directory(args.input_dir, args.framework)
    
    # 2. Generate Report
    report_md = generate_markdown_report(catalog)
    
    # 3. Write to Step Summary (always visible in Actions UI)
    step_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary_file:
        with open(step_summary_file, "a") as f:
            f.write(report_md + "\n")
            
    # 4. Post to PR if applicable
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    gh_token = os.environ.get("GH_TOKEN")
    
    if event_path and gh_token:
        with open(event_path, "r") as f:
            event_data = json.load(f)
            
        if "pull_request" in event_data:
            pr_number = event_data["pull_request"]["number"]
            repo_full_name = event_data["repository"]["full_name"]
            
            print(f"Detected PR #{pr_number}. Posting comment...")
            post_pr_comment(repo_full_name, pr_number, gh_token, report_md)
        else:
            print("Not a pull request event. Skipping PR comment.")
            
    # Fail the action if coverage drops below 100% (or some threshold) ?
    # For now, just exit 0 so we don't block merges aggressively.
    sys.exit(0)

if __name__ == "__main__":
    main()
