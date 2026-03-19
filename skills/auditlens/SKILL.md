---
name: auditlens
description: "Cross-platform GRC engine for automated audit readiness and gap analysis. Maps organizational evidence to ISO 27001, SOC 2, HIPAA, and NIST CSF. Provides automated classification, maturity scoring, and interactive audit workspaces with local privacy guardrails."
---

# AuditLens — Enterprise Compliance Analysis Engine

An intelligent compliance analysis engine that reads organizational documents, maps them to regulatory frameworks, identifies gaps, scores maturity, and produces an interactive audit workspace.

## 🛡️ Privacy & Data Security

Mandatory check: Refer to `references/privacy_guardrails.md` before processing evidence.

### Pre-Flight Protocol
- **Detection**: Identify deployment tier (Enterprise/Commercial/Consumer).
- **Safety**: Flag if model training is enabled; recommend Incognito for consumer plans.
- **Classification**: Assign sensitivity tier (Critical/High/Medium/Low).
- **Redaction**: Execute local PII/PHI scrubbing before document ingestion.

## Enterprise Connectors

Before any analysis, detect available connectors. Read `references/connectors.md` for full integration details.

**Google Workspace** — via `gws` CLI (`@googleworkspace/cli`):
- Drive: Scan evidence folders, download docs, export Sheets/Docs
- Gmail: Search for policy acknowledgments, training completions
- Calendar: Verify management review cadence
- Auth: `gws auth setup && gws auth login -s drive,docs,sheets,gmail,calendar`

**Microsoft 365** — via `m365` CLI (`@pnp/cli-microsoft365`):
- OneDrive/SharePoint: Scan document libraries, download evidence files
- Entra ID: Pull user/group/app data for access control evidence
- Purview: Get sensitivity labels, retention policies
- Teams/Planner: Collaboration governance, remediation task tracking
- Auth: `m365 setup && m365 login`

**Claude MCP Connectors** (auto-detected in Claude.ai):
- Google Drive MCP → `google_drive_search` / `google_drive_fetch`
- Gmail MCP → search for compliance-relevant communications
- Linear MCP → track remediation tasks
- PostHog MCP → product analytics for processing integrity evidence

**Connector Detection** — at session start:
```bash
command -v gws >/dev/null 2>&1 && echo "GWS available"
command -v m365 >/dev/null 2>&1 && echo "M365 available"
```

If neither CLI is available, fall back to Claude MCP connectors or direct file uploads.

## 🛠️ Core Capabilities

1. **Evidence Cataloging**: Automated classification of documents by control domain and framework tagging.
2. **Gap Analysis**: Comparison of evidence against target controls; status: Evidenced, Weak, Missing, or Stale.
3. **Cross-Framework Mapping**: Unified mapping to satisfy multiple regulatory requirements with single artifacts.
4. **Maturity Scoring**: CMMI-aligned 1-5 rating based on procedural depth and execution evidence.
5. **Audit Workspace**: Generation of an interactive, self-contained HTML environment for auditor review.
6. **Remediation Roadmap**: Prioritized action items with effort-impact matrix.

## Step 0: Read Framework References and Connector Docs

Before doing ANY analysis, read the relevant reference files:

### Framework Control Catalogs
```
references/
├── iso27001.md        — ISO 27001:2022 Annex A controls (93 controls)
├── soc2.md            — SOC 2 Trust Service Criteria (61 criteria)
├── hipaa.md           — HIPAA Security Rule safeguards (46 specs)
├── gdpr.md            — GDPR Articles mapped to controls
├── nist_csf.md        — NIST CSF 2.0 categories (22 categories)
├── pci_dss.md         — PCI DSS v4.0 requirements
├── crosswalk.md       — Cross-framework control mapping table
├── connectors.md      — Enterprise connector reference (gws, m365, MCP)
├── advanced_usecases.md — 12 novel capabilities beyond standard compliance
```

Read the relevant file(s) based on which framework(s) the user selected. If they haven't chosen yet, ask which framework(s) they need — or suggest based on their industry/context.

## Step 1: Ingest and Classify Documents

### Reading uploaded files
Use the file-reading skill patterns to handle whatever the user provides:
- PDFs → extract text via pypdf or pdftotext
- DOCX → pandoc to markdown
- XLSX/CSV → pandas for structured data
- Folders → walk directory tree and process each file
- Google Drive → use drive search tools if available

### Classification approach
For each document, determine:
1. **Document type**: Policy, Procedure, Standard, Guideline, Record, Evidence artifact, Training material, Risk assessment, Vendor agreement, Configuration export, Log sample, Screenshot
2. **Control domains it covers** (map to the framework's control areas)
3. **Evidence strength**: Direct (explicitly addresses a control), Indirect (partially supports), Weak (tangentially related)
4. **Freshness**: Extract dates, flag anything >12 months old as potentially stale

Run the classification script to produce structured output:

```bash
python3 /path/to/skill/scripts/classify_evidence.py \
  --input-dir /mnt/user-data/uploads/ \
  --framework iso27001 \
  --output /home/claude/compliance-workspace/evidence_catalog.json
```

If the script isn't available or the scenario is simpler, do the classification inline by reading each document and producing the same JSON structure.

### Evidence catalog JSON structure
```json
{
  "framework": "ISO 27001:2022",
  "scan_date": "2025-03-19",
  "documents": [
    {
      "filename": "InfoSec-Policy-v3.pdf",
      "doc_type": "Policy",
      "control_mappings": [
        {"control_id": "A.5.1", "control_name": "Policies for information security", "strength": "direct"},
        {"control_id": "A.5.2", "control_name": "Information security roles", "strength": "indirect"}
      ],
      "last_updated": "2024-08-15",
      "freshness": "current",
      "summary": "Organization-wide information security policy covering scope, roles, and objectives.",
      "key_excerpts": ["Section 3.1 defines ISMS scope...", "Section 5 assigns CISO responsibilities..."]
    }
  ],
  "unmapped_documents": [],
  "statistics": {
    "total_documents": 24,
    "mapped_documents": 21,
    "unmapped_documents": 3,
    "control_coverage_pct": 68.5,
    "stale_documents": 4
  }
}
```

## Step 2: Gap Analysis

Compare the evidence catalog against the full control set of the chosen framework. For each control:

| Status | Meaning |
|--------|---------|
| ✅ Evidenced | At least one direct-strength document maps here |
| ⚠️ Weak | Only indirect or weak evidence exists |
| ❌ Missing | No evidence at all |
| 🔄 Stale | Evidence exists but is >12 months old |

### Gap report structure
Group gaps by control domain/clause. For each gap, include:
- **Control ID and name**
- **Risk level**: Critical / High / Medium / Low (based on the control's typical audit weight)
- **Remediation suggestion**: What document or artifact would close this gap
- **Effort estimate**: Quick Win (< 1 week), Moderate (1-4 weeks), Significant (1-3 months), Major (3+ months)
- **Cross-framework impact**: Which other frameworks this gap also affects

## Step 3: Maturity Scoring

Score each control domain on the CMMI-inspired scale:

| Level | Name | Criteria |
|-------|------|----------|
| 1 | Initial | No documented process, ad-hoc |
| 2 | Managed | Some documentation exists but incomplete |
| 3 | Defined | Policies + procedures documented and approved |
| 4 | Quantitatively Managed | Evidence of measurement, metrics, reviews |
| 5 | Optimizing | Continuous improvement cycle documented |

Base the score on:
- Document completeness (does the policy exist?)
- Procedural depth (are there SOPs, not just policy?)
- Evidence of execution (logs, screenshots, records)
- Review cadence (dated reviews, version history)
- Measurement (metrics, KPIs, dashboards)

## Step 4: Generate Outputs

The user may want any combination of these outputs:

### A. Summary Report (Markdown or DOCX)
Use the docx skill if they want a Word document. Structure:
- Executive Summary with overall readiness score
- Framework coverage heatmap (by domain)
- Top 10 critical gaps
- Maturity scores by domain
- Remediation roadmap
- Appendix: Full evidence catalog

### B. Interactive Audit Workspace (HTML)
This is the flagship output. Generate using the template in `assets/audit_viewer_template.html`.

The audit workspace provides:
- **Framework navigator** — sidebar with all control domains, color-coded by status
- **Control detail panel** — shows control description, mapped evidence, gap status
- **Evidence viewer** — click any evidence item to see summary and key excerpts
- **Cross-framework view** — toggle to see how controls map across frameworks
- **Comment system** — auditors can add notes per control (persisted in localStorage)
- **Export** — download the full assessment as JSON or generate a PDF summary
- **Filter bar** — filter by status (gap/evidenced/stale), risk level, domain
- **Maturity dashboard** — radar chart showing maturity scores per domain

Build this as a self-contained HTML file with embedded CSS and JS (no external dependencies except CDN libraries). Use:
- Tailwind via CDN for layout
- Chart.js via CDN for the maturity radar chart
- Clean, professional aesthetic — no emoji overload, muted color palette with status accents

### C. Remediation Tracker (XLSX)
Use the xlsx skill. Columns:
- Control ID | Control Name | Status | Risk Level | Gap Description | Remediation Action | Owner (blank) | Due Date (blank) | Effort | Cross-Framework Impact | Notes

## Step 5: Cross-Framework Intelligence (Bonus Workflows)

These are advanced capabilities that set this skill apart:

### 5a. Control Crosswalk Generator
When a user is certified in one framework and pursuing another, show which controls carry over. Read `references/crosswalk.md` and generate a mapping that shows:
- Controls already satisfied by existing evidence
- New controls unique to the target framework
- Delta effort to reach the new certification

### 5b. Audit Interview Prep
Generate likely auditor questions for each control domain based on the framework. For weak/missing areas, suggest talking points and compensating controls. Output as a structured prep document.

### 5c. Evidence Freshness Monitor
Scan all evidence and produce a timeline showing:
- What needs renewal in the next 30/60/90 days
- What's already stale
- Suggested review cadence per document type

### 5d. Vendor/Third-Party Risk Mapping
If the user uploads vendor questionnaires or SIG responses, map vendor controls against the organization's framework requirements and flag coverage gaps in the supply chain.

### 5e. Policy Generation from Gaps
For critical gaps where no policy exists, offer to draft a starter policy document that addresses the control requirements. Use the docx skill to produce a professional template.

## Step 6: Advanced Capabilities (Beyond Standard GRC)

For these advanced use cases, read `references/advanced_usecases.md` for full implementation details.

### 6a. Compliance Drift Detection
Compare current evidence against a previous audit snapshot. Surfaces what CHANGED — new gaps opened, evidence went stale, coverage regressed. Output a severity-scored drift report.

### 6b. AI-Powered Control Narrative Generation
Auto-generate the auditor-ready paragraphs that describe HOW the org implements each control. The #1 time-sink in audit prep — this creates first drafts from actual evidence.

### 6c. Regulatory Change Impact Analysis
When a framework releases a new version (ISO 2013→2022, PCI 3.2.1→4.0), auto-map existing controls to the new version and identify net-new requirements vs. carried-forward.

### 6d. Shadow IT Discovery
Analyze evidence gaps + identity data to find undocumented systems. Unmanaged OAuth apps, external sharing, orphaned service accounts, ungoverned groups.

### 6e. Compliance-as-Code Linting
Analyze Terraform/CloudFormation/K8s manifests for compliance violations. Maps findings to specific framework controls with file/line references and fix suggestions.

### 6f. Compliance Inheritance Mapping (Shared Responsibility)
For cloud deployments, map which controls the provider handles vs. shared vs. customer-owned. Prevents the "we assumed AWS covered that" audit failure.

### 6g. Board-Ready Compliance Storytelling
Translate technical control data into business risk language. Maps controls to financial impact, generates executive dashboards with trend lines and peer comparisons.

### 6h. Natural Language Audit Query
Let auditors ask plain English questions: "When was the access review last performed?" and get instant answers from the evidence catalog.

### 6i. Cross-Org Compliance Benchmarking
For multi-subsidiary orgs, compare maturity scores across business units. Identify weak links, share best practices.

### 6j. Predictive Non-Compliance
Based on evidence aging and historical drift, predict which controls will fall out of compliance in 30/60/90 days. Shift from reactive to predictive.

### 6k. Evidence Provenance Chain
Track complete lifecycle: who created, reviewed, approved each artifact. Version history, storage locations, control mappings. Auditors increasingly demand this.

### 6l. Automated Vendor Security Scoring
Ingest SIG/CAIQ questionnaires, score vendor posture, map vendor controls against org framework requirements, generate risk tiering.

## 💎 Execution Standards

1. **Strict Veracity**: Never hallucinate evidence. If a requirement is unmet, mark as a High-Risk Gap.
2. **Technical Precision**: Provide exact control IDs and specific remediation tasks.
3. **Maturity Objectivity**: Score based on observable evidence, not subjective intent.
4. **Temporal Context**: Every finding must include a timestamp and version reference.
5. **Terminology Alignment**: Adapt to organizational nomenclature found in source documents.
6. **Granular Mapping**: Explicitly state which paragraphs in which files satisfy specific control criteria.
7. **Efficiency**: Use local processing (`classify_evidence.py`) for large datasets to minimize token overhead.
