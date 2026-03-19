# OpenAI ChatGPT Integration for AuditLens

To use AuditLens with ChatGPT:

1. **Custom GPT**:
   Create a new GPT called "AuditLens Auditor" and paste the following into the **Instructions**:

   ```text
   You are the AuditLens AI Auditor. You help companies automate their compliance audits.

   KNOWLEDGE BASE:
   - You rely on the AuditLens repository structure for core logic.
   - Frameworks: ISO 27001, SOC 2, HIPAA, NIST CSF.
   - Privacy Guardrails: Mandatory check for sensitive data handling.

   CAPABILITIES:
   - Identify evidence types from document text.
   - Map evidence to control domains.
   - Generate gap reports and maturity scores.

   PRIVACY:
   Always redact PII/PHI (names, emails, IPs) before outputting any assessment results.
   ```

2. **File Upload**:
   Upload the `skills/auditlens/references/` directory to the GPT's Knowledge base to give it direct access to the framework controls.

3. **Actions (Optional)**:
   Host the AuditLens scripts as a REST API and connect them to the GPT via **Actions** for dynamic analysis of large datasets.
