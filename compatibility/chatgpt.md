# ChatGPT Integration

### Setup

1. Create a new GPT in ChatGPT, name it **"AuditLens Auditor"**
2. Paste the contents of `skill/SKILL.md` into the **Instructions** field
3. Upload all files from `skill/references/` to the **Knowledge** section

### Usage

```
"Check if we're SOC 2 ready — here are our policy documents"
"Analyze this vendor questionnaire for security gaps"
"What HIPAA safeguards are we missing?"
```

### Privacy

The GPT follows the privacy guardrails defined in `skill/references/privacy_guardrails.md` and will redact PII/PHI before outputting assessment results.
