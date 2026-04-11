# Acme Corp — Information Security Policy
**Document ID**: POL-001
**Version**: 3.2
**Owner**: Sarah Chen, CISO
**Approved by**: James Rodriguez, CEO
**Last Review**: 2026-02-15
**Next Review**: 2026-08-15

## 1. Purpose
This policy establishes the framework for protecting the confidentiality, integrity, and availability of Acme Corp's information assets, including customer data processed through the Acme CDP platform.

## 2. Scope
This policy applies to all employees, contractors, and third-party personnel who access Acme Corp information systems. It covers all data environments including production (AWS us-east-1, eu-west-1), staging, development, and corporate systems.

## 3. Information Security Principles
- **Least Privilege**: Access is granted on a need-to-know basis.
- **Defense in Depth**: Multiple layers of security controls are maintained.
- **Separation of Duties**: Critical functions require multiple approvals.
- **Continuous Monitoring**: All systems are monitored 24/7 via Datadog SIEM.

## 4. Roles and Responsibilities
| Role | Responsibility |
|------|---------------|
| CISO (Sarah Chen) | Overall security program ownership |
| VP Engineering (Mark Liu) | Secure development lifecycle |
| IT Manager (Priya Patel) | Endpoint and infrastructure security |
| HR Director (David Kim) | Personnel security and training |
| DPO (Elena Vasquez) | Data privacy and GDPR compliance |

## 5. Access Control
- All access requires Okta SSO with MFA enforced.
- Privileged access requires manager approval + security team review.
- Access reviews conducted quarterly by team leads.
- Terminated employee access revoked within 24 hours of HR notification.

## 6. Data Classification
| Level | Description | Examples |
|-------|-------------|---------|
| Restricted | Customer PII, financial data, credentials | CDP datasets, API keys, database credentials |
| Confidential | Internal business data | Revenue reports, product roadmap, employee data |
| Internal | General business information | Meeting notes, project plans |
| Public | Approved for external sharing | Marketing materials, public docs |

## 7. Incident Response
- All security incidents reported to security@acmecorp.io or Slack #security-incidents.
- P1 incidents: 15-minute response SLA, CEO/CISO notification within 1 hour.
- P2 incidents: 4-hour response SLA.
- Post-incident review within 5 business days.
- Customer notification within 72 hours for data breaches (per GDPR/contractual requirements).

## 8. Acceptable Use
- Company devices must have CrowdStrike Falcon and MDM (Jamf/Intune) active.
- Personal devices may not access production systems.
- All code changes require peer review via GitHub pull requests.
- Secrets must be stored in HashiCorp Vault — never in code or config files.

## 9. Compliance
Acme Corp maintains compliance with:
- SOC 2 Type II (Security, Availability, Confidentiality)
- ISO 27001:2022
- GDPR (EU customer data)
- CCPA (California customer data)

## 10. Policy Violations
Violations of this policy may result in disciplinary action up to and including termination. All violations are documented and reported to the CISO.

---
*Signatures on file. Digital acknowledgment tracked via BambooHR.*
