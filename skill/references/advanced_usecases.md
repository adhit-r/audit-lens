# Advanced Use Cases — Beyond Standard Compliance

These capabilities differentiate this skill from every GRC tool on the market. They leverage the unique position of an AI agent sitting between document stores, code repositories, identity systems, and human conversations.

## Table of Contents
1. [Compliance Drift Detection](#drift)
2. [AI-Powered Control Narrative Generation](#narratives)
3. [Regulatory Change Impact Analysis](#reg-change)
4. [Shadow IT Discovery via Evidence Gaps](#shadow-it)
5. [Compliance-as-Code Linting](#compliance-code)
6. [Compliance Inheritance Mapping (Shared Responsibility)](#inheritance)
7. [Board-Ready Compliance Storytelling](#board-ready)
8. [Natural Language Audit Query Engine](#nl-query)
9. [Cross-Org Compliance Benchmarking](#benchmarking)
10. [Predictive Non-Compliance Detection](#predictive)
11. [Evidence Provenance Chain](#provenance)
12. [Automated Vendor Security Scoring](#vendor-scoring)

---

## 1. Compliance Drift Detection {#drift}

**What it does**: Compares the current evidence catalog against a "golden snapshot" from the last successful audit. Surfaces what drifted — new gaps that opened, evidence that went stale, controls that lost coverage.

**Why it's novel**: Traditional GRC tools show point-in-time status. This shows the delta — what CHANGED since your auditor last signed off.

### Implementation

1. After each successful audit, save the full assessment JSON as a versioned snapshot:
   ```
   snapshots/
   ├── 2024-Q4-soc2-audit.json
   ├── 2025-Q2-soc2-surveillance.json
   ```

2. On next run, diff the current catalog against the most recent snapshot:
   - **New gaps**: Controls that were evidenced but are now missing
   - **Stale drift**: Documents that were current but are now past their review date
   - **Coverage regression**: Evidence strength downgraded (direct → indirect)
   - **Positive drift**: New evidence added, gaps closed since last audit

3. Output a drift report with severity scoring:
   - Critical: Previously evidenced control is now completely missing
   - High: Evidence went stale (>12 months since last review)
   - Medium: Evidence strength downgraded
   - Low: Minor metadata changes

**Trigger phrases**: "What changed since our last audit?", "Show me compliance drift", "Compare current state to our SOC 2 report from Q4"

---

## 2. AI-Powered Control Narrative Generation {#narratives}

**What it does**: Auto-generates auditor-ready control narratives from raw evidence documents. These are the paragraphs auditors need that describe HOW an organization implements each control — not just WHAT the policy says.

**Why it's novel**: Writing control narratives is the #1 time sink in audit prep. Every SOC 2 and ISO audit requires 50-100+ narratives describing control implementation. This generates first drafts from actual evidence.

### Narrative Template

For each control, generate:

```
[CONTROL ID]: [Control Name]

CONTROL OBJECTIVE:
[What this control is meant to achieve — from the framework]

CONTROL DESCRIPTION:
[How the organization implements this control — generated from evidence]

EVIDENCE OF OPERATION:
- [Specific document/artifact that demonstrates implementation]
- [Second evidence artifact with date and relevance]

TESTING APPROACH:
[How an auditor would verify this control is operating — inquiry, observation, inspection, reexecution]

IDENTIFIED EXCEPTIONS:
[Any gaps or deviations noted during analysis — or "None identified"]
```

### Quality Criteria
- Use the organization's own terminology (pulled from their documents)
- Reference specific sections/pages of evidence
- Include dates and version numbers
- Note who is responsible (if identifiable from evidence)
- Flag where narrative needs human review

**Trigger phrases**: "Generate control narratives for our SOC 2", "Write the control descriptions for the auditor", "Draft our ISO statement of applicability"

---

## 3. Regulatory Change Impact Analysis {#reg-change}

**What it does**: When a compliance framework releases a new version (e.g., ISO 27001:2013 → 2022, PCI DSS 3.2.1 → 4.0, NIST CSF 1.1 → 2.0), automatically maps the organization's existing controls to the new version and identifies net-new requirements.

**Why it's novel**: Framework migrations are expensive consulting engagements. This provides the analysis in minutes.

### Process

1. Load both the old and new framework control sets
2. Map existing evidence to the OLD framework controls
3. Apply the official transition mapping (e.g., ISO 27001 Annex A correlation table)
4. Identify:
   - **Carried forward**: Controls that map directly to the new version (no action needed)
   - **Merged**: Multiple old controls collapsed into one new control
   - **Split**: One old control expanded into multiple new controls
   - **Net-new**: Entirely new requirements with no predecessor
   - **Retired**: Old controls no longer required

5. For net-new requirements, assess:
   - Do any existing documents partially cover it?
   - What's the effort to close the gap?
   - What peer organizations typically use as evidence?

**Trigger phrases**: "We need to migrate from ISO 2013 to 2022", "What changed in PCI DSS v4?", "How do we transition to NIST CSF 2.0?"

---

## 4. Shadow IT Discovery via Evidence Gaps {#shadow-it}

**What it does**: Analyzes patterns in evidence gaps and cross-references with identity/access data to identify undocumented systems, applications, or processes that fall outside the compliance scope.

**Why it's novel**: Traditional compliance focuses on what's IN scope. This finds what SHOULD be in scope but isn't.

### Detection Signals

From Google Workspace / M365 analysis:
- **Unmanaged OAuth apps**: `gws` or `m365` can list connected third-party apps
- **External sharing**: Documents shared outside the org without classification
- **Ungoverned groups/channels**: Teams/Spaces without owners or retention policies
- **App registrations without owners**: Service accounts nobody claims

From evidence gap analysis:
- Asset inventory says 50 systems, but only 30 have security configurations documented
- Access reviews cover 10 applications, but SSO shows 25 active integrations
- Vendor register lists 15 vendors, but contracts folder has 40 vendor agreements

### Output
A "shadow IT risk report" showing:
- Undocumented systems discovered
- Ungoverned data sharing patterns
- Orphaned service accounts
- Recommended scope additions

**Trigger phrases**: "What's missing from our scope?", "Find shadow IT", "Are there systems we're not tracking?"

---

## 5. Compliance-as-Code Linting {#compliance-code}

**What it does**: Analyzes infrastructure-as-code (Terraform, CloudFormation, Kubernetes manifests, Dockerfiles) for compliance violations — then maps findings to specific framework controls.

**Why it's novel**: Bridges the gap between DevOps and GRC. Instead of "you have a misconfigured S3 bucket," says "S3 bucket `prod-logs` violates ISO A.8.24 (Cryptography) and SOC 2 CC6.7 (Data Transmission) because server-side encryption is not enabled."

### What to Lint

| IaC Pattern | Compliance Control | Check |
|------------|-------------------|-------|
| S3 bucket without encryption | A.8.24, CC6.7 | `server_side_encryption_configuration` present |
| Security group with 0.0.0.0/0 ingress | A.8.20, CC6.5 | No unrestricted inbound rules |
| RDS without backup retention | A.8.13, A1.2 | `backup_retention_period > 0` |
| IAM user with inline policy | A.5.15, CC6.1 | No inline policies on users |
| CloudTrail disabled | A.8.15, CC7.2 | CloudTrail enabled in all regions |
| EBS volume unencrypted | A.8.24, CC6.7 | `encrypted = true` |
| No VPC flow logs | A.8.16, CC7.2 | Flow logs enabled |
| Public subnet for databases | A.8.22, CC6.6 | Database subnets are private |

### Output
Structured findings with:
- File path and line number
- IaC resource identifier
- Compliance control(s) violated
- Severity (based on control risk weight)
- Suggested fix (code snippet)

**Trigger phrases**: "Check our Terraform for compliance issues", "Lint our infrastructure code against SOC 2", "Are our CloudFormation templates compliant?"

---

## 6. Compliance Inheritance Mapping (Shared Responsibility) {#inheritance}

**What it does**: For organizations using cloud services (AWS, GCP, Azure) or SaaS platforms, maps which controls are fully handled by the provider, which are shared, and which are entirely the customer's responsibility.

**Why it's novel**: Every cloud audit starts with "what does the provider cover?" This automates the shared responsibility decomposition.

### Inheritance Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Fully Inherited** | Provider handles completely, customer inherits via provider's certification | Physical security (A.7.x) on AWS |
| **Shared** | Provider handles platform-level, customer handles application-level | Encryption: AWS provides KMS, customer must enable it |
| **Customer-Owned** | Provider has no role, fully customer's responsibility | Security awareness training, HR screening |
| **Complementary** | Provider offers a capability, customer must configure it | Logging: CloudTrail exists, customer must enable and monitor |

### Process
1. Identify which cloud providers/SaaS platforms are in scope
2. Load the provider's compliance documentation (SOC 2 report, ISO cert)
3. Map each framework control to an inheritance category
4. For "shared" and "complementary" controls, document what the customer MUST do
5. Highlight controls where the customer assumes they're covered but aren't

**Trigger phrases**: "What does AWS cover for our SOC 2?", "Map our shared responsibility with GCP", "Which controls do we still own on Azure?"

---

## 7. Board-Ready Compliance Storytelling {#board-ready}

**What it does**: Translates technical compliance data into executive-level dashboards and narratives that boards and C-suite can actually understand. Maps controls to business risk and financial impact.

**Why it's novel**: CISOs struggle to communicate compliance posture to non-technical leadership. This creates the translation layer.

### Output Format

Instead of "A.8.24 Cryptography — 65% coverage", produce:

> **Data Protection Risk: MODERATE**
> 65% of our systems that handle sensitive customer data have encryption properly configured and documented. The remaining 35% represents ~12 systems including our customer portal and analytics pipeline. If these systems experienced a data breach, estimated exposure is $2.4M based on our cyber insurance assessment. Remediation is in progress with an ETA of Q3 2025.

### Dashboard Elements
- Risk heatmap (not control heatmap — BUSINESS risk)
- Trend lines (are we getting better or worse?)
- Peer comparison (how do similar companies perform?)
- Investment ROI (cost of compliance vs. cost of non-compliance)
- Regulatory deadline timeline

**Trigger phrases**: "Prepare a board presentation on our compliance posture", "Translate this for the CEO", "Executive summary of our audit readiness"

---

## 8. Natural Language Audit Query Engine {#nl-query}

**What it does**: Lets auditors ask questions in plain English and get instant answers from the evidence catalog.

**Why it's novel**: Auditors spend days hunting through document repositories. This gives them a conversational interface to the entire evidence set.

### Example Queries

| Auditor Asks | System Does |
|-------------|-------------|
| "Show me all encryption-related controls and their evidence" | Filters catalog for A.8.24, CC6.7, §164.312(a)(2)(iv) |
| "When was the access review last performed?" | Searches for access review reports, returns dates |
| "Who approved the information security policy?" | Extracts approval metadata from policy documents |
| "Are there any controls that depend on manual processes?" | Analyzes evidence for automation vs. manual indicators |
| "What evidence do we have for business continuity?" | Returns all BCP/DR related documents with freshness |
| "Which vendor agreements are missing security clauses?" | Cross-references vendor contracts against required terms |

**Trigger phrases**: "I need to ask questions about our evidence", "Set up an audit query session", "Help me find evidence for..."

---

## 9. Cross-Org Compliance Benchmarking {#benchmarking}

**What it does**: For organizations with multiple subsidiaries, business units, or franchise locations, compares compliance posture across entities to identify weak links.

**Why it's novel**: Enterprise GRC is siloed. This creates a unified view across organizational boundaries.

### Output
- Heatmap comparing maturity scores across business units
- Identify which unit is the weakest link (relevant for group certifications)
- Share best practices: "Unit A's access review process scored 4.5/5 — Unit C should adopt it"
- Aggregate risk view for the parent company

---

## 10. Predictive Non-Compliance Detection {#predictive}

**What it does**: Based on evidence aging patterns and historical drift data, predicts which controls are likely to fall out of compliance in the next 30/60/90 days.

**Why it's novel**: Shifts compliance from reactive ("we failed the audit") to predictive ("we'll fail in 60 days if we don't act now").

### Prediction Signals
- Document review dates approaching expiry
- Employee terminations without corresponding access revocation (from HRIS data)
- Vulnerability scan reports getting older
- Training completion rates declining
- Vendor contract renewal dates approaching

---

## 11. Evidence Provenance Chain {#provenance}

**What it does**: Tracks the complete lifecycle of each evidence artifact — who created it, when it was last reviewed, who approved it, where it's stored, and how it maps to controls.

**Why it's novel**: Auditors increasingly ask about evidence provenance, not just evidence existence.

### Provenance Record
```json
{
  "evidence_id": "EVD-2025-042",
  "filename": "InfoSec-Policy-v3.pdf",
  "created_by": "jane.smith@company.com",
  "created_date": "2024-03-15",
  "last_reviewed_by": "john.doe@company.com",
  "last_reviewed_date": "2025-01-20",
  "approved_by": "ciso@company.com",
  "approved_date": "2025-01-25",
  "storage_locations": [
    "Google Drive: /Compliance/Policies/",
    "SharePoint: /sites/compliance/Shared Documents/"
  ],
  "version_history": [
    {"version": "3.0", "date": "2024-03-15", "change": "Annual review and update"},
    {"version": "2.1", "date": "2023-06-01", "change": "Added cloud security section"}
  ],
  "control_mappings": ["A.5.1", "CC5.3", "§164.316(a)"]
}
```

---

## 12. Automated Vendor Security Scoring {#vendor-scoring}

**What it does**: Ingests vendor security questionnaires (SIG, CAIQ, custom), scores vendor security posture, and maps vendor controls against the organization's own framework requirements.

**Why it's novel**: Vendor risk assessment is the most painful compliance activity. This automates the scoring and gap identification.

### Process
1. Ingest vendor questionnaire responses (CSV, XLSX, or PDF)
2. Parse responses by control domain
3. Score each domain (based on response completeness and quality)
4. Map vendor controls to the organization's framework
5. Flag gaps: "Vendor X doesn't address encryption at rest, which is required for your ISO A.8.24"
6. Generate a vendor risk tier: Critical / High / Medium / Low

### Integration with Vendor Management
- Track vendor scores over time
- Alert when vendor certifications expire
- Compare vendors side-by-side for procurement decisions

**Trigger phrases**: "Score this vendor questionnaire", "How does this vendor compare to our requirements?", "Which vendors are our riskiest?"
