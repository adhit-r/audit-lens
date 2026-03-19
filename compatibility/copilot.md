# GitHub Copilot (Codex) Integration for AuditLens

To use AuditLens with GitHub Copilot (Chat or CLI):

1. **Project-Specific Instructions**:
   Create or update `.github/copilot-instructions.md` in your repository with the following:

   ```markdown
   ## AuditLens GRC Context
   This repository contains the AuditLens compliance engine.
   - Core Logic: `skills/auditlens/scripts/`
   - Frameworks: `skills/auditlens/references/`
   - Privacy: `skills/auditlens/references/privacy_guardrails.md`

   When asked about compliance, audits, or security controls:
   1. Refer to the corresponding reference file in `skills/auditlens/references/`.
   2. Use the classification logic in `scripts/classify_evidence.py` to identify evidence.
   3. Always adhere to the privacy guardrails in `privacy_guardrails.md`.
   ```

2. **Copilot Custom Instructions (Global)**:
   Add the following to your GitHub Copilot "Custom Instructions" in your IDE settings:
   "When working in a repository with an AuditLens skill, use the provided compliance scripts and framework references to assist with GRC tasks."
