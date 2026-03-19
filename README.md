# 🔍 AuditLens

**Hardware-accelerated GRC & Compliance Intelligence for AI Agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://code.claude.com)
[![SKILL.md](https://img.shields.io/badge/Open%20Standard-SKILL.md-green)](https://github.com/anthropics/skills)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/adhit-r/audit-lens.svg?style=social)](https://github.com/adhit-r/audit-lens/stargazers)

AuditLens provides a technical infrastructure for automating GRC (Governance, Risk, and Compliance) workflows. It maps organizational evidence to high-fidelity control sets—ISO 27001, SOC 2, HIPAA, and NIST CSF—delivering automated gap analysis, maturity scoring, and interactive audit workspaces.

## ⚡️ Key Advantages

- **Integrated GRC**: Native execution within Claude Code, Gemini, and ChatGPT.
- **Privacy-First Heuristics**: Localized PII/PHI detection and redaction; no sensitive data exfiltration.
- **Unified Crosswalk**: Single-evidence mapping across 5+ frameworks simultaneously.
- **Deterministic Analysis**: Data-driven gap identification with remediation effort estimates.

> Works with Claude Code, Claude.ai, Cowork, and any agent supporting the SKILL.md open standard.

## Quick Install

**Claude Code (plugin):**
```bash
/plugin marketplace add adhit-r/audit-lens
```

**Claude Code (manual):**
```bash
git clone https://github.com/adhit-r/audit-lens.git
cp -r audit-lens/skills/auditlens ~/.claude/skills/
```

**Claude.ai:** Download `auditlens.skill` from [Releases](../../releases) and upload in Settings.

## What It Does

Drop your compliance evidence (PDFs, DOCX, XLSX, CSV, or scan from Google Drive / SharePoint) and pick a framework.

### Core Workflows

| # | Capability | What Happens |
|---|-----------|-------------|
| 1 | **Evidence Catalog** | Classifies every document by type, maps to control domains |
| 2 | **Gap Analysis** | Compares against full control set — missing, weak, stale |
| 3 | **Cross-Framework Mapping** | Map once, comply many — one control satisfies ISO + SOC 2 + HIPAA |
| 4 | **Maturity Scoring** | CMMI-inspired 1-5 score per domain |
| 5 | **Audit Workspace** | Interactive HTML viewer with navigation, comments, radar chart, export |
| 6 | **Remediation Tracker** | Prioritized action list with effort estimates |

### Advanced Capabilities

| # | Capability | What Makes It Different |
|---|-----------|----------------------|
| 7 | **Compliance Drift Detection** | What CHANGED since last audit — not just point-in-time |
| 8 | **Control Narrative Generation** | Auto-drafts the 50-100 paragraphs auditors need |
| 9 | **Regulatory Change Impact** | Framework migration analysis in minutes |
| 10 | **Shadow IT Discovery** | Finds what SHOULD be in scope but isn't |
| 11 | **Compliance-as-Code Linting** | Maps Terraform/CloudFormation violations to controls |
| 12 | **NL Audit Query Engine** | Auditors ask plain English, get instant answers |
| 13 | **Evidence Provenance Chain** | Full lifecycle: who created, reviewed, approved |
| 14 | **Vendor Security Scoring** | Auto-score SIG/CAIQ questionnaires, risk tier vendors |
| 15 | **Board-Ready Storytelling** | Translates controls → business risk for C-suite |
| 16 | **Predictive Non-Compliance** | Predicts which controls fail in 30/60/90 days |
| 17 | **Shared Responsibility Mapping** | AWS/GCP/Azure inherited vs customer-owned controls |
| 18 | **Cross-Org Benchmarking** | Compare maturity across subsidiaries |

---

## 🤖 Multi-Agent Compatibility

AuditLens is designed as a cross-platform skill that can be loaded into any modern AI agent.

| Agent | Integration Guide | Method |
|-------|-------------------|--------|
| **Claude Code** | [Method 1](INSTALL.md) | Native Plugin / SKILL.md |
| **Antigravity** | [antigravity.md](compatibility/antigravity.md) | Native / Project Skill |
| **GitHub Copilot** | [copilot.md](compatibility/copilot.md) | Custom Instructions |
| **Google Gemini** | [gemini.md](compatibility/gemini.md) | Gems / System Prompt |
| **OpenAI ChatGPT** | [chatgpt.md](compatibility/chatgpt.md) | Custom GPTs |

### Model Context Protocol (MCP)

For agents that support the [Model Context Protocol](https://modelcontextprotocol.io), you can run the AuditLens MCP server to expose compliance tools directly to your agent:

```bash
python3 skills/auditlens/scripts/mcp_server.py
```

This exposes `classify_evidence`, `audit_query`, `track_provenance`, and `score_vendor` as tools.

| Platform | Tool | What It Scans |
|----------|------|--------------|
| Google Workspace | [`gws` CLI](https://github.com/googleworkspace/cli) | Drive folders, Docs, Sheets, Gmail, Calendar |
| Microsoft 365 | [`m365` CLI](https://github.com/pnp/cli-microsoft365) | OneDrive, SharePoint, Entra ID, Purview, Teams |
| Claude.ai | Native MCP | Google Drive, Gmail, Calendar, Linear |

## Privacy Guardrails

This skill handles sensitive enterprise data. Built-in privacy architecture includes:

- **Mandatory pre-flight privacy check** before processing any documents
- **Sensitivity classification** (Critical/High/Medium/Low) with proportional data handling
- **PII/PHI detection and redaction** before processing
- **Data minimization** — summarize and classify, never echo full document content
- **Post-session cleanup reminders** for consumer plan users
- **Deployment recommendations** by data sensitivity tier

| Deployment | Training? | Retention | Recommended For |
|-----------|----------|-----------|-----------------|
| Enterprise API + ZDR | No | None | Pen test reports, vuln scans |
| Commercial API | No | 30 days | Policies, procedures, risk registers |
| Consumer + safeguards | Opt-out | 30 days | Quick assessments only |

See [`references/privacy_guardrails.md`](skills/auditlens/references/privacy_guardrails.md) for the full privacy architecture.

## Frameworks Supported

| Framework | Controls | Reference File |
|-----------|---------|---------------|
| ISO 27001:2022 | 93 Annex A controls | `references/iso27001.md` |
| SOC 2 TSC | 61 criteria | `references/soc2.md` |
| HIPAA Security Rule | 46 safeguards | `references/hipaa.md` |
| NIST CSF 2.0 | 22 categories (106 subcategories) | `references/nist_csf.md` |
| PCI DSS v4.0 | Coming soon | — |
| GDPR | Coming soon | — |

Cross-framework mapping in `references/crosswalk.md`.

## Repo Structure

```
auditlens/
├── .claude-plugin/
│   └── plugin.json                          Plugin manifest
├── marketplace.json                         Marketplace catalog
├── skills/
│   └── auditlens/
│       ├── SKILL.md                         Core skill (306 lines)
│       ├── scripts/
│       │   ├── classify_evidence.py         Document classifier
│       │   ├── audit_query_engine.py        NL query engine
│       │   ├── evidence_provenance.py       Lifecycle tracker
│       │   └── vendor_scorer.py             Vendor questionnaire scorer
│       ├── references/
│       │   ├── iso27001.md                  93 Annex A controls
│       │   ├── soc2.md                      61 Trust Service Criteria
│       │   ├── hipaa.md                     46 Security Rule safeguards
│       │   ├── nist_csf.md                  22 CSF 2.0 categories
│       │   ├── crosswalk.md                 Cross-framework mapping
│       │   ├── connectors.md                Enterprise connector reference
│       │   ├── privacy_guardrails.md        Data privacy architecture
│       │   └── advanced_usecases.md         18 advanced capabilities
│       └── assets/
│           └── audit_viewer_template.html   Interactive audit workspace
├── INSTALL.md                               5 installation methods
├── LICENSE                                  MIT
└── README.md
```

## Example Prompts

```
"Check if we're SOC 2 ready — here are our policy documents"

"Analyze these uploaded files against ISO 27001 and show me the gaps"

"Score this vendor security questionnaire against our framework"

"What changed since our last audit in Q4?"

"Which controls are shared between our SOC 2 and ISO 27001?"

"Generate control narratives for the auditor"

"What evidence do we have for encryption?"
```

## Optional: Enterprise CLI Setup

```bash
# Google Workspace
npm install -g @googleworkspace/cli
gws auth setup && gws auth login -s drive,docs,sheets,gmail,calendar

# Microsoft 365
npm install -g @pnp/cli-microsoft365
m365 setup && m365 login
```

The skill auto-detects available connectors at runtime.

## Contributing

PRs welcome. Priorities:
- Additional framework references (PCI DSS v4.0, GDPR, SOX, FedRAMP)
- Improved classification accuracy
- More enterprise connector integrations
- Additional audit workspace features

## License

MIT — see [LICENSE](LICENSE)

---

Built by [Adhithya Rajasekaran](https://github.com/adhit-r) | Powered by the SKILL.md open standard
