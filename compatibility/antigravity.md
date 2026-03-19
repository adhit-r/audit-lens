# Antigravity Integration for AuditLens

Antigravity natively supports the `SKILL.md` standard. To use AuditLens with Antigravity:

1. **Local Skill Loading**:
   Copy the `skills/auditlens` directory to your project's `.claude/skills/` folder.
   ```bash
   cp -r skills/auditlens .claude/skills/
   ```

2. **System Prompt Alignment**:
   You can also provide this context to Antigravity in your session:
   "I am using the AuditLens GRC engine. Please refer to `skills/auditlens/SKILL.md` for our compliance workflows, privacy guardrails, and available scripts for document classification and gap analysis."

3. **Direct Execution**:
   Antigravity can run the Python scripts in `skills/auditlens/scripts/` directly to perform high-fidelity analysis without sending sensitive document contents to the model.
