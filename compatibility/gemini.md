# Google Gemini Integration for AuditLens

To use AuditLens with Google Gemini (via Vertex AI, AI Studio, or Gemini Advanced):

1. **Gemini Advanced (Gems)**:
   Create a new Gem called "AuditLens Compliance Officer" with the following instructions:
   
   ```text
   You are an expert GRC Auditor using the AuditLens engine.
   Your goal is to help your organization achieve and maintain compliance.

   CORE KNOWLEDGE:
   - Use the scripts in `skills/auditlens/scripts/` for evidence processing.
   - Reference the control sets in `skills/auditlens/references/` (ISO 27001, SOC 2, HIPAA, NIST CSF).
   - Strictly follow the `privacy_guardrails.md`.

   WORKFLOW:
   1. Ask for the compliance framework to assess against.
   2. Process uploaded evidence using the classification heuristics in the scripts.
   3. Identify gaps and provide remediation advice.
   ```

2. **Vertex AI / AI Studio**:
   Paste the content of `skills/auditlens/SKILL.md` into the "System Instructions" field of your Chat Prompt or Agent configuration.

3. **MCP Support**:
   If using a Gemini-powered IDE or agent that supports the Model Context Protocol (MCP), connect the AuditLens MCP server (see `scripts/mcp_server.py`).
