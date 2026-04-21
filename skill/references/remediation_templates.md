# AuditLens Remediation Templates

This file contains auditor-approved boilerplate templates for generating missing compliance policies.
When executing **Step 5e (Evidence Generation)**, you MUST use these templates as the structural foundation.
Do not hallucinate policy structures.

## Instruction to Agent
When drafting a document based on these templates:
1. Replace `[ORG_NAME]` with the actual organization name.
2. Replace `[CISO/ROLE]` with the appropriate title based on company size.
3. Replace all `<INSERT: ...>` blocks with intelligent, contextually appropriate text based on what you learned during the evidence ingestion phase (e.g., if the company uses AWS and Okta, mention AWS and Okta in the Access Control policy).
4. ALWAYS include the "Document Governance" table at the top of the file.

---

## 0. Document Governance (Mandatory Header)

```markdown
# [POLICY_NAME]

## Document Governance
| Attribute | Detail |
|-----------|--------|
| **Document Owner** | [CISO/ROLE] |
| **Classification** | Internal |
| **Version** | 1.0 (Auto-Generated Draft) |
| **Last Updated** | [CURRENT_DATE] |
| **Next Review Due** | [CURRENT_DATE + 365 DAYS] |

*Generated via AuditLens Remediation Engine*
```

---

## 1. Information Security Policy
**Maps to:** ISO 27001 (A.5.1), SOC 2 (CC1.1, CC1.2), NIST CSF (GV.PO-01)

```markdown
[INSERT GOVERNANCE HEADER]

## 1. Purpose
The purpose of this Information Security Policy is to establish the framework for managing and protecting the information assets of [ORG_NAME]. It ensures the confidentiality, integrity, and availability (CIA) of systems and data.

## 2. Scope
This policy applies to all employees, contractors, consultants, temporaries, and other workers at [ORG_NAME], including all personnel affiliated with third parties. This policy applies to all equipment that is owned or leased by [ORG_NAME].

## 3. Roles and Responsibilities
- **Management**: Responsible for approving this policy and allocating resources.
- **[CISO/ROLE]**: Responsible for implementing and monitoring compliance.
- **Employees**: Responsible for adhering to this policy and reporting suspected violations.

## 4. Policy Directives
### 4.1 Data Protection
All [ORG_NAME] data must be classified according to the Data Classification Policy. Sensitive data must be encrypted at rest and in transit.
<INSERT: Briefly mention DB and transit encryption standards used by the org>

### 4.2 Acceptable Use
Information systems are provided for business purposes. Personnel must not use systems in a manner that violates laws or endangers [ORG_NAME].

### 4.3 Incident Reporting
All personnel must immediately report suspected security incidents to the [CISO/ROLE] via <INSERT: Ticketing system or email, e.g., security@[ORG_NAME].com>.

## 5. Enforcement
Violations of this policy may result in disciplinary action up to and including termination of employment and legal action.
```

---

## 2. Logical Access Control Policy
**Maps to:** SOC 2 (CC6.1 - CC6.8), ISO 27001 (A.9.1), HIPAA (164.312(a)(1))

```markdown
[INSERT GOVERNANCE HEADER]

## 1. Purpose
To establish rules for the granting, modification, and revocation of access to [ORG_NAME]'s information systems based on the Principle of Least Privilege.

## 2. Provisioning & Deprovisioning
### 2.1 Onboarding
Access to systems is granted only upon verified request from HR or the hiring manager.
<INSERT: Describe the identity provider provisioning flow, e.g., BambooHR to Okta SCIM>

### 2.2 Offboarding
Access must be immediately revoked upon an employee's termination. Standard SLA for complete revocation across all corporate systems is 24 hours.

## 3. Authentication Requirements
- **Passwords**: Passwords must be a minimum of 14 characters and stored securely.
- **Multi-Factor Authentication (MFA)**: MFA is strictly required for all administrative access, VPN access, and access to systems containing customer data.
<INSERT: Mention specific IdP used for MFA, e.g., Okta Verify, Duo>

## 4. Access Reviews
The [CISO/ROLE] will conduct a formal system access review covering all critical systems <INSERT: Insert Frequency, e.g., quarterly>.
```

---

## 3. Incident Response Plan
**Maps to:** SOC 2 (CC7.3), NIST IR (RS.MA-01), ISO 27001 (A.16.1)

```markdown
[INSERT GOVERNANCE HEADER]

## 1. Purpose
This procedure defines the steps [ORG_NAME] will take to detect, respond to, and recover from cybersecurity incidents.

## 2. Incident Response Phases (NIST Framework)
### 2.1 Preparation
[ORG_NAME] maintains security monitoring tools including <INSERT: List monitoring tools, e.g., AWS CloudWatch, CrowdStrike> and conducts annual tabletop exercises.

### 2.2 Identification
Any anomalous behavior flagged by users or security tooling must be evaluated by the Security Team to declare an incident.

### 2.3 Containment
Immediate actions must be taken to isolate the threat. This may include disconnecting compromised hosts from the network or disabling user credentials.

### 2.4 Eradication
The root cause must be identified and removed. Affected systems must be patched or rebuilt.

### 2.5 Recovery
Systems are restored from clean backups <INSERT: Mention backup utility> and returned to production.

### 2.6 Lessons Learned
Within 14 days of a major incident, a Post-Incident Report (PIR) must be generated and discussed by management.

## 3. Severity Matrix
| Severity | Description | Target Response Time | 
|----------|-------------|----------------------|
| Sev 0 | Critical breach / Complete outage | 15 minutes |
| Sev 1 | High risk / Partial outage | 1 hour |
| Sev 2 | Medium risk / Single user compromised | 4 hours |
| Sev 3 | Low risk / Phishing attempt | 24 hours |
```

---

## 4. AI Acceptable Use Policy
**Maps to:** ISO 42001 (A.2), NIST AI RMF

```markdown
[INSERT GOVERNANCE HEADER]

## 1. Purpose
To ensure that Generative AI and Large Language Models (LLMs) are used safely, ethically, and securely within [ORG_NAME].

## 2. Approved AI Tools
Employees may only use AI tools that have been formally vetted and approved by the [CISO/ROLE].
<INSERT: List approved tools based on evidence, e.g., Enterprise ChatGPT (no training), GitHub Copilot>

## 3. Data Sensitivity Rules
- **Public Data**: May be freely used in any AI tool.
- **Internal Data**: May only be used in approved Enterprise AI tools where data training is explicitly disabled.
- **Customer / PII Data**: STRICTLY PROHIBITED from being entered into any public or third-party AI tool without explicit DPAddendums.

## 4. Output Verification
AI-generated code, text, or decisions must be reviewed by a human prior to use in production or external communication. AI tools are assistants, not authoritative sources.
```
