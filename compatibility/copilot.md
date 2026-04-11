# GitHub Copilot Integration

### Setup

Add the following to `.github/copilot-instructions.md`:

```markdown
## AuditLens Compliance Context

This project uses AuditLens for compliance analysis.
- Framework references: `skill/references/`
- Privacy guardrails: `skill/references/privacy_guardrails.md`
- Audit viewer template: `skill/assets/audit_viewer_template.html`

When asked about compliance, audit readiness, or gap analysis:
1. Read the relevant framework reference files before analysis
2. Follow the workflow in `skill/SKILL.md`
3. Adhere strictly to `privacy_guardrails.md` for PII/PHI handling
```

Then copy the skill into your project:

```bash
cp -r skill/ ./skill/
```

### Usage

```
"Check our compliance posture against ISO 27001"
"Review this PR for compliance impact"
"What policies are we missing for SOC 2?"
```
