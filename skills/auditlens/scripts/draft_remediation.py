#!/usr/bin/env python3
"""
AuditLens Remediation Drafter
Generates baseline compliance policy and procedure templates to accelerate gap remediation.
"""

import json
import sys
import argparse
import datetime

TEMPLATES = {
    "A.5": """# Information Security Policy
## 1. Objective
To provide management direction and support for information security in accordance with business requirements and relevant laws and regulations.

## 2. Scope
This policy applies to all employees, contractors, temporary staff, and third parties accessing corporate information systems.

## 3. Principles
- Information must be protected against unauthorized access.
- Confidentiality of information must be assured.
- Integrity of information must be maintained.
- Regulatory and legislative requirements must be met.

## 4. Responsibilities
Management is responsible for defining and approving the security policy. All personnel are responsible for adhering to this policy.

*Document Date: {date}*
""",
    "A.9": """# Access Control Policy
## 1. Objective
To limit access to corporate information and processing facilities to authorized users only.

## 2. User Access Provisioning
- Access rights are granted based on the principle of least privilege.
- A formal process must be followed for granting and revoking access.
- Access rights must be reviewed at regular intervals (e.g., quarterly).

## 3. Authentication & Passwords
- Multi-Factor Authentication (MFA) is strictly enforced for all systems.
- Passwords must be at least 14 characters long and rotated every 90 days.

*Document Date: {date}*
""",
    "A.12": """# Operational Security Procedure
## 1. Objective
To ensure correct and secure operations of information processing facilities.

## 2. Malware Protection
- Centrally managed anti-malware software must be installed on all endpoints.
- Scans must be executed weekly.

## 3. Backup Protocol
- Critical databases must be backed up daily.
- Backups must be tested for restoration feasibility on a bi-annual basis.

*Document Date: {date}*
"""
}

def draft_policy(domain_id: str, framework: str = "iso27001", company_name: str = "Acme Corp"):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Simple heuristic to extract SOC2 vs ISO IDs
    # E.g., SOC2 CC6 vs ISO A.9
    
    template = TEMPLATES.get(domain_id)
    if not template:
        template = f"""# Compliance Policy for {domain_id}

## 1. Objective
To ensure adherence to {framework.upper()} requirements regarding control domain {domain_id}.

## 2. Standard Operating Procedures
[This is an auto-generated baseline. Please detail the specific organizational requirements, roles, and technical safeguards implemented to address {domain_id}.]

## 3. Enforcement
Violations of this policy will be subject to disciplinary action.

*Document Date: {today}*
"""
    else:
        template = template.format(date=today)
        
    template = template.replace("corporate", f"{company_name}'s")

    result = {
        "status": "success",
        "domain_id": domain_id,
        "framework": framework,
        "draft_content": template,
        "suggested_filename": f"draft_{domain_id.replace('.', '_')}_{framework}.md"
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Draft baseline compliance policies")
    parser.add_argument("domain_id", help="The control domain ID (e.g., A.5, CC6)")
    parser.add_argument("--framework", default="iso27001", help="Target framework")
    parser.add_argument("--company", default="Acme Corp", help="Company name for template")
    args = parser.parse_args()

    try:
        draft = draft_policy(args.domain_id, args.framework, args.company)
        print(json.dumps(draft))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
