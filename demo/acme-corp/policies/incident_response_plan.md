# Acme Corp — Incident Response Plan
**Document ID**: POL-IR-001
**Version**: 2.0
**Owner**: Sarah Chen, CISO
**Last Review**: 2026-01-20
**Last Test**: 2025-11-15 (tabletop exercise)

## 1. Incident Classification

| Severity | Description | Response SLA | Escalation |
|----------|-------------|-------------|------------|
| P1 — Critical | Data breach, system compromise, ransomware | 15 minutes | CISO + CEO within 1 hour |
| P2 — High | Unauthorized access attempt, vulnerability exploited | 4 hours | CISO within 4 hours |
| P3 — Medium | Policy violation, phishing click (no compromise) | 24 hours | IT Manager |
| P4 — Low | False positive, informational alert | 72 hours | SOC analyst |

## 2. Incident Response Team

| Role | Primary | Backup |
|------|---------|--------|
| Incident Commander | Sarah Chen (CISO) | Mark Liu (VP Eng) |
| Technical Lead | Alex Thompson (Sr. Security Eng) | Ravi Sharma (DevOps Lead) |
| Communications | Elena Vasquez (DPO) | James Rodriguez (CEO) |
| Legal | Outside counsel: Wilson & Sommer LLP | Sarah Chen |

## 3. Response Phases

### 3.1 Detection & Triage
- CrowdStrike Falcon alerts → PagerDuty → on-call engineer
- Datadog security monitors → Slack #security-alerts
- Employee reports → security@acmecorp.io or Slack #security-incidents

### 3.2 Containment
- Isolate affected systems (CrowdStrike network containment)
- Revoke compromised credentials (Okta session revocation)
- Block malicious IPs (Cloudflare WAF)

### 3.3 Eradication & Recovery
- Root cause analysis within 48 hours
- Patch/remediate vulnerability
- Restore from AWS Backup if data corruption occurred

### 3.4 Post-Incident Review
- PIR document within 5 business days
- Lessons learned shared in engineering all-hands
- Control improvements tracked in Jira project: SECURITY

## 4. Communication Plan
- Internal: Slack #security-incidents (real-time), email summary (end of day)
- Customer: notification within 72 hours per GDPR Art. 33, via email from DPO
- Regulatory: within 72 hours to relevant DPA (EU), 60 days to HHS (if HIPAA-covered)
- Board: quarterly security report with incident summary

## 5. Incident Log (Q1 2026)

| Date | Severity | Description | Resolution | Time to Resolve |
|------|----------|-------------|------------|-----------------|
| 2026-01-08 | P3 | Phishing email clicked by 2 employees, no credential compromise | Accounts locked, passwords reset, additional training assigned | 2 hours |
| 2026-02-14 | P2 | S3 bucket misconfiguration — public read access on staging bucket | Bucket policy corrected, no customer data exposed (staging only) | 1.5 hours |
| 2026-03-22 | P4 | CrowdStrike false positive on internal tool | Exclusion added after validation | 30 minutes |
