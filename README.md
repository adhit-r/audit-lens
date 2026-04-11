<div align="center">
  <img src="skill/assets/logo.png" width="160" height="160" alt="AuditLens Logo">
  <h1>AuditLens</h1>
  <p>The enterprise agentic compliance engine.</p>
  
  <p>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
    <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  </p>
  
  <p align="center">
    <a href="#quick-start">Quick Start</a> •
    <a href="#how-it-works">How It Works</a> •
    <a href="#v2-enterprise-capabilities">Features</a> •
    <a href="#multi-agent-support">Install</a> •
    <a href="CONTRIBUTING.md">Contributing</a>
  </p>
</div>

---

## What is AuditLens?

AuditLens is an **agent skill** — expert instructions, policy templates, and framework references that turn any AI agent into a precision compliance auditor and active remediation engine.

No keyword matching. No heuristics. Your AI agent reads your documents, reasons about their content against regulatory frameworks, automatically drafts missing policies, and produces auditor-grade HTML workspaces.

## Quick Start

### Claude Code

```bash
/plugin marketplace add adhit-r/audit-lens
```

### Any Other Agent

```bash
git clone https://github.com/adhit-r/audit-lens.git
```

Then copy `skill/` into your agent's skill directory. See [Multi-Agent Support](#multi-agent-support) for platform-specific paths.

### Start Auditing

Once installed, ask your agent:

```
"Audit my evidence folder against ISO 27001"
"Check our SOC 2 readiness"
"Score this vendor's SIG questionnaire"
```

## How It Works

AuditLens is **not a standalone tool** — it's pure intelligence that lives inside your AI agent.

```
┌────────────┐     ┌─────────────────────┐     ┌────────────────┐
│ Your Docs  │ ──→ │ AI Agent + AuditLens│ ──→ │ Dual-View HTML │
│ (evidence) │     │ (Orchestrator)      │     │ Dashboards     │
└────────────┘     └─────────────────────┘     └────────────────┘
```

The agent:
1. **Ingests** your organizational documents (policies, procedures, logs, configs).
2. **References** the framework control catalogs (ISO 27001, SOC 2, etc.).
3. **Maps** evidence to specific controls with strength ratings.
4. **Identifies gaps** and **Auto-Remediates** missing policies.
5. **Generates** two interactive audit workspaces (GRC & Auditor).

## V2 Enterprise Capabilities 🚀

AuditLens V2 transforms the skill from a simple gap-analyzer into a full-fledged enterprise compliance platform.

### 1. Automated Remediation Engine
When a gap is found, the agent doesn't just flag it—it writes the fix. Powered by `remediation_templates.md`, the agent automatically generates auditor-approved, contextually-injected draft policies (e.g., ISO InfoSec Policies, Incident Response Plans) ready for management signature.

### 2. Open Security Architecture (OSA) Cascade
"Test once, comply with many." AuditLens maps your evidence against the NIST-based OSA catalog, automatically cascading your compliance status across 87+ global frameworks (ISO, SOC 2, HIPAA, GDPR, DORA) simultaneously. 

### 3. Dual UI Workspaces
The agent generates two interactive, self-contained HTML files:
* **The GRC Dashboard**: A *Vanta-styled*, high-level readiness overview for executives and compliance teams.
* **The Auditor Workspace**: An *Overdrive-enhanced*, brutalist data-matrix for external auditors featuring View Transitions and deep-dive JSON payloads.

### 4. Ecosystem Auto-Discovery
AuditLens understands modern SaaS stacks. It maps over 50+ integrations (AWS, Okta, GitHub, Datadog) directly to specific control requirements via the `ecosystem_connectors.md` reference.

## Supported Frameworks

| Framework | Controls | Reference |
|-----------|----------|-----------|
| ISO 27001:2022 | 93 Annex A controls | `skill/references/iso27001.md` |
| SOC 2 Type II | 61 trust service criteria | `skill/references/soc2.md` |
| HIPAA | 46 safeguard specifications | `skill/references/hipaa.md` |
| NIST CSF 2.0 | 22 categories | `skill/references/nist_csf.md` |
| PCI DSS v4.0 | Payment card requirements | `skill/references/pci_dss.md` |
| GDPR | Data protection articles | `skill/references/gdpr.md` |

## Multi-Agent Support

AuditLens works with any AI agent that can read files and follow instructions.

| Platform | Install |
|----------|---------|
| **Claude Code** | `/plugin marketplace add adhit-r/audit-lens` |
| **Antigravity** | `cp -r skill/ .agents/skills/auditlens/` |
| **Gemini** | Paste `skill/SKILL.md` into System Instructions |
| **ChatGPT** | Paste `skill/SKILL.md` into Custom GPT, upload `skill/references/` |
| **Copilot** | Append context from `skill/SKILL.md` to `.github/copilot-instructions.md` |

Detailed guides: [Antigravity](compatibility/antigravity.md) · [Gemini](compatibility/gemini.md) · [ChatGPT](compatibility/chatgpt.md) · [Copilot](compatibility/copilot.md)

## Repository Structure

```
audit-lens/
├── skill/                    ← The agent skill
│   ├── SKILL.md              ← Agent instructions
│   ├── references/           ← Framework catalogs & Ecosystem/OSA mappings
│   │   ├── remediation_templates.md  ← Boilerplates for Auto-Remediation
│   │   ├── ecosystem_connectors.md   ← SaaS mapping logic
│   │   └── ... framework definitions
│   └── assets/               
│       ├── grc_viewer_template.html     ← Executive Dashboard UI
│       └── auditor_viewer_template.html ← Deep-Dive Matrix UI
├── compatibility/            ← Per-agent install guides
└── demo/                     ← Synthetic test environment (Acme Corp)
```

Zero code. Pure content. The agent is the intelligence.

## Contributing

See [Contributing Guide](CONTRIBUTING.md).

---

<p align="center">
  Developed by <a href="https://github.com/AdhithyaRajasekaran">Adhithya Rajasekaran</a>
</p>
