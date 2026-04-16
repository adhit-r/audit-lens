import os
import json
import datetime

BASE_DIR = "/Users/adhi/axonome/Compliance-master-skill/audit-lens/demo/acme-corp"
POLICIES_DIR = os.path.join(BASE_DIR, "policies")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(POLICIES_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. GENERATE POLICIES
policies = {
    "information_security_policy.md": "# Information Security Policy\n\n## 1. Purpose\nEstablishes the foundation for Acme Corp's ISMS, ensuring CIA triad protection. \n\n## 2. Scope\nApplies to all employees, contractors, and production AWS environments.\n\n## 3. Leadership\nThe CISO is ultimately responsible for the ISMS.",
    "acceptable_use_policy.md": "# Acceptable Use Policy\n\n## 1. Acceptable Use\nCompany equipment (managed via Jamf) is for business purposes. Personal use must be limited.\n\n## 2. Prohibited Uses\nNo torrenting, illegal activities, or circumventing Kandji MDM controls.",
    "access_control_policy.md": "# Access Control Policy\n\n## 1. Provisioning\nAll access is provisioned via BambooHR -> Okta SCIM. \n\n## 2. Authentication\nMFA is strictly enforced via Okta Verify for all apps.",
    "incident_response_plan.md": "# Incident Response Plan\n\n## 1. Phases\nPreparation, Identification, Containment, Eradication, Recovery, Lessons Learned.\n\n## 2. SLA\nSev0 requires 15min response. Handled via PagerDuty and Jira.",
    "business_continuity_plan.md": "# Business Continuity Plan\n\n## 1. RTO/RPO\nRecovery Time Objective is 4 hours. Recovery Point Objective is 1 hour.\n\n## 2. Backups\nAWS RDS backups run hourly. S3 cross-region replication is active.",
    "data_classification_policy.md": "# Data Classification Policy\n\n## 1. Tiers\nPublic, Internal, Confidential, Restricted (Customer PII/PHI).\n\n## 2. Handling\nRestricted data must never leave the AWS VPC and must be encrypted at rest utilizing KMS.",
    "cryptography_policy.md": "# Cryptography Policy\n\n## 1. Algorithms\nAES-256 for data at rest. TLS 1.2+ for in-transit.\n\n## 2. Key Management\nAWS KMS is authoritative. Keys are automatically rotated every 365 days.",
    "vendor_management_policy.md": "# Vendor Management Policy\n\n## 1. Assessment\nAll vendors must complete a SIG Core or present a SOC 2 Type II report before processing Acme data.\n\n## 2. Reviews\nCritical vendors are reassessed annually.",
    "sdlc_policy.md": "# Secure SDLC Policy\n\n## 1. Methodology\nAgile sprints. All code requires peer review (1 approval minimum on GitHub).\n\n## 2. Testing\nSAST (SonarQube) and SCA (Dependabot) run on all PRs.",
    "change_management_policy.md": "# Change Management Policy\n\n## 1. Approvals\nAll infrastructure and code changes must have a Jira Change Request and be approved by the CAB.\n\n## 2. Emergency Changes\nAllowed in Sev0 scenarios but require retrospective Jira tracking.",
    "physical_security_policy.md": "# Physical Security Policy\n\n## 1. Offices\nAcme Corp uses WeWork offices. Badge access is managed by WeWork.\n\n## 2. Data Centers\nAWS data centers handles all physical security per SOC 2 inheritance.",
    "hr_security_policy.md": "# HR Security Policy\n\n## 1. Screening\nCheckr is used for pre-employment background checks.\n\n## 2. Training\nKnowBe4 compliance training is mandated within 30 days of hire and annually."
}

for name, content in policies.items():
    with open(os.path.join(POLICIES_DIR, name), "w") as f:
        f.write(content)

# 2. GENERATE API MOCKS
reports = {
    "bamboohr_employee_directory.json": json.dumps([
        {"empId": "100", "status": "Active", "department": "Engineering", "isContractor": False},
        {"empId": "101", "status": "Terminated", "terminationDate": "2026-03-10", "department": "Sales"}
    ], indent=2),
    "jira_change_tickets.json": json.dumps([
        {"issueId": "CHG-104", "status": "Done", "approver": "cab-group", "linkedPr": "github.com/acme/core/pull/200"},
        {"issueId": "CHG-105", "status": "Pending", "approver": None, "linkedPr": "github.com/acme/core/pull/201"}
    ], indent=2),
    "aws_security_hub.json": json.dumps({
        "findings": [
            {"id": "s3-encryption", "status": "PASSED", "resource": "arn:aws:s3:::acme-prod-data"},
            {"id": "iam-mfa", "status": "PASSED", "resource": "arn:aws:iam::123456789:root"}
        ]
    }, indent=2),
    "okta_system_log.json": json.dumps({
        "events": [
            {"action": "user.session.start", "outcome": "SUCCESS", "mfaUsed": "Okta Verify"},
            {"action": "user.lifecycle.deactivate", "target": "empId_101", "actor": "BambooHR_SCIM"}
        ]
    }, indent=2),
    "jamf_mdm_compliance.json": json.dumps({
        "totalDevices": 450,
        "encrypted": 450,
        "osUpToDate": 432,
        "passwordRequired": 450
    }, indent=2)
}

for name, content in reports.items():
    with open(os.path.join(REPORTS_DIR, name), "w") as f:
        f.write(content)

# 3. GENERATE AUDIT CATALOG (ASSESSMENT DATA)
catalog = {
  "framework": "ISO 27001:2022",
  "scan_date": "2026-04-12",
  "controls": [
    {
      "id": "A.5.1",
      "name": "Policies for information security",
      "status": "evidenced",
      "evidence": [{"filename": "information_security_policy.md", "strength": "direct", "summary": "Core InfoSec policy"}]
    },
    {
      "id": "A.5.15",
      "name": "Access control",
      "status": "evidenced",
      "evidence": [
        {"filename": "access_control_policy.md", "strength": "direct", "summary": "Provisioning limits"},
        {"filename": "okta_system_log.json", "strength": "corroborating", "summary": "API logs prove SCIM deprovisioning"}
      ]
    },
    {
      "id": "A.5.21",
      "name": "Information security in ICT supply chain",
      "status": "evidenced",
      "evidence": [{"filename": "vendor_management_policy.md", "strength": "direct", "summary": "SIG/SOC2 requirement"}]
    },
    {
      "id": "A.8.12",
      "name": "Data leakage prevention",
      "status": "evidenced",
      "evidence": [{"filename": "aws_security_hub.json", "strength": "corroborating", "summary": "S3 buckets encrypted and not public"}]
    },
    {
      "id": "A.8.25",
      "name": "Secure development lifecycle",
      "status": "evidenced",
      "evidence": [
        {"filename": "sdlc_policy.md", "strength": "direct", "summary": "PR mandate"},
        {"filename": "jira_change_tickets.json", "strength": "corroborating", "summary": "Jira tracks PR links and CAB approval"}
      ]
    },
    {
      "id": "A.8.15",
      "name": "Logging",
      "status": "evidenced",
      "evidence": [{"filename": "aws_security_hub.json", "strength": "direct", "summary": "CloudTrail active"}]
    },
    {
      "id": "A.6.2",
      "name": "Terms and conditions of employment",
      "status": "evidenced",
      "evidence": [
        {"filename": "hr_security_policy.md", "strength": "direct", "summary": "Stipulates checks"},
        {"filename": "bamboohr_employee_directory.json", "strength": "corroborating", "summary": "Active employee list tracked"}
      ]
    },
    {
      "id": "A.5.9",
      "name": "Inventory of information and other associated assets",
      "status": "missing",
      "description": "Inventory of all assets and their owners required.",
      "remediation": "Deploy Asset Tracker MDM connection."
    },
    {
      "id": "A.8.20",
      "name": "Networks security",
      "status": "missing",
      "description": "Network configurations and firewall rules.",
      "remediation": "Document AWS Security Groups architecture."
    }
  ],
  "statistics": {
    "total_documents": 17,
    "mapped_documents": 17,
    "control_coverage_pct": 91.5
  }
}

with open(os.path.join(OUTPUT_DIR, "evidence_catalog.json"), "w") as f:
    f.write(json.dumps(catalog, indent=2))

# 4. GENERATE HTML DASHBOARDS
final_json_str = json.dumps(catalog)

import re

# GRC
with open("/Users/adhi/axonome/Compliance-master-skill/audit-lens/skill/assets/grc_viewer_template.html", "r") as f:
    grc = f.read()
grc = re.sub(r'const ASSESSMENT_DATA = .*?;', f'const ASSESSMENT_DATA = {final_json_str};', grc)
with open(os.path.join(OUTPUT_DIR, "acme_grc_dashboard.html"), "w") as f:
    f.write(grc)

# Auditor
with open("/Users/adhi/axonome/Compliance-master-skill/audit-lens/skill/assets/auditor_viewer_template.html", "r") as f:
    aud = f.read()
aud = re.sub(r'const ASSESSMENT_DATA = .*?;', f'const ASSESSMENT_DATA = {final_json_str};', aud)
with open(os.path.join(OUTPUT_DIR, "acme_auditor_workspace.html"), "w") as f:
    f.write(aud)

print("Massive Payload Generated successfully.")
