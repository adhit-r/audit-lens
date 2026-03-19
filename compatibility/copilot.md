# GitHub Copilot (Codex)

### Configuration
Update `.github/copilot-instructions.md`:

```markdown
## AuditLens GRC Context
- Core Logic: `skills/auditlens/scripts/`
- Frameworks: `skills/auditlens/references/`
- Privacy: `skills/auditlens/references/privacy_guardrails.md`

Rules:
1. Reference `skills/auditlens/references/` for control sets.
2. Use `scripts/classify_evidence.py` for document processing.
3. Adhere to `privacy_guardrails.md` for PII/PHI handling.
```
