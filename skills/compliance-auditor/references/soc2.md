# SOC 2 — Trust Service Criteria Reference

## Table of Contents
1. [CC — Common Criteria (Security)](#cc)
2. [A — Availability](#availability)
3. [PI — Processing Integrity](#pi)
4. [C — Confidentiality](#confidentiality)
5. [P — Privacy](#privacy)

---

## CC — Common Criteria (Security) {#cc}

### CC1 — Control Environment

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC1.1 | COSO Principle 1: Demonstrates commitment to integrity and ethical values | Code of conduct, ethics policy, whistleblower program |
| CC1.2 | COSO Principle 2: Board exercises oversight responsibility | Board meeting minutes, governance charter |
| CC1.3 | COSO Principle 3: Management establishes structure, authority, responsibility | Org chart, RACI matrix, role descriptions |
| CC1.4 | COSO Principle 4: Demonstrates commitment to competence | Job descriptions, training records, certifications |
| CC1.5 | COSO Principle 5: Enforces accountability | Performance reviews, disciplinary records |

### CC2 — Communication and Information

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC2.1 | COSO Principle 13: Uses relevant quality information | Internal reporting, metrics dashboards |
| CC2.2 | COSO Principle 14: Communicates internally | Internal comms, policy distribution records |
| CC2.3 | COSO Principle 15: Communicates externally | External comms policy, customer notifications |

### CC3 — Risk Assessment

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC3.1 | COSO Principle 6: Specifies suitable objectives | Risk assessment methodology, security objectives |
| CC3.2 | COSO Principle 7: Identifies and analyzes risks | Risk register, risk assessment reports |
| CC3.3 | COSO Principle 8: Assesses fraud risk | Fraud risk assessment, anti-fraud controls |
| CC3.4 | COSO Principle 9: Identifies and analyzes significant change | Change management process, change risk assessment |

### CC4 — Monitoring Activities

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC4.1 | COSO Principle 16: Selects and develops monitoring activities | Monitoring procedures, dashboards, KPIs |
| CC4.2 | COSO Principle 17: Evaluates and communicates deficiencies | Internal audit reports, remediation tracking |

### CC5 — Control Activities

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC5.1 | COSO Principle 10: Selects and develops control activities | Control catalog, risk-control mapping |
| CC5.2 | COSO Principle 11: Selects and develops general controls over technology | IT general controls documentation |
| CC5.3 | COSO Principle 12: Deploys through policies and procedures | Policy library, procedure documents |

### CC6 — Logical and Physical Access Controls

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC6.1 | Logical access security software, infrastructure, architectures | Access control policy, network diagrams, RBAC config |
| CC6.2 | Prior to issuing credentials, registers and authorizes new users | User provisioning procedures, approval workflows |
| CC6.3 | Access to credentials is based on authorization and authenticated | Authentication policy, MFA configuration |
| CC6.4 | Access to protected information assets is restricted and reviewed | Access reviews, user access reports |
| CC6.5 | Logical access security measures against threats from external sources | Firewall configs, IDS/IPS, WAF configurations |
| CC6.6 | Restrict access to system components from outside boundaries | Network segmentation, VPN configuration |
| CC6.7 | Restricts transmission, movement, removal of information | DLP configuration, data transfer policies |
| CC6.8 | Controls against threats from malicious software | AV/EDR deployment, email security |

### CC7 — System Operations

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC7.1 | Uses defined configuration baselines | Hardening standards, configuration baselines |
| CC7.2 | Monitors system components for anomalies | SIEM configuration, monitoring alerts |
| CC7.3 | Evaluates security events | Event triage procedures, incident classification |
| CC7.4 | Responds to identified security incidents | Incident response plan, playbooks, post-mortems |
| CC7.5 | Identifies and develops remediation activities | Remediation tracking, vulnerability management |

### CC8 — Change Management

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC8.1 | Changes to infrastructure and software are authorized, designed, developed, tested | Change management policy, CAB records, test evidence |

### CC9 — Risk Mitigation

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| CC9.1 | Identifies and assesses risk from business relationships | Vendor risk assessment, third-party risk management |
| CC9.2 | Assesses and manages risks associated with vendors and partners | Vendor due diligence reports, contract reviews |

## A — Availability {#availability}

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| A1.1 | Maintains, monitors, and evaluates current processing capacity | Capacity planning, performance monitoring |
| A1.2 | Authorizes, designs, develops, implements, and operates environmental protections | BCP/DR plans, redundancy architecture |
| A1.3 | Tests recovery plan procedures | DR test results, recovery time documentation |

## PI — Processing Integrity {#pi}

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| PI1.1 | Obtains or generates, uses, and communicates relevant quality information | Data validation rules, input/output controls |
| PI1.2 | Implements policies and procedures over system processing | Processing procedures, reconciliation records |
| PI1.3 | Implements policies for inputs, processing, and outputs | Error handling procedures, data quality checks |
| PI1.4 | Implements policies for storage of data | Data retention policy, archival procedures |
| PI1.5 | Monitors for processing integrity errors | Monitoring dashboards, error tracking |

## C — Confidentiality {#confidentiality}

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| C1.1 | Identifies and maintains confidential information | Data classification policy, confidential data inventory |
| C1.2 | Disposes of confidential information | Data disposal procedures, destruction certificates |

## P — Privacy {#privacy}

| Criteria ID | Criteria | Typical Evidence |
|------------|---------|-----------------|
| P1.1 | Privacy notice provided | Privacy notice/policy, consent records |
| P2.1 | Choice and consent mechanisms | Consent management, opt-out mechanisms |
| P3.1 | Personal information collected for identified purposes | Data collection procedures, purpose limitation |
| P3.2 | Consent for new purposes | Consent management for secondary use |
| P4.1 | Collection limited to identified purposes | Data minimization procedures |
| P4.2 | Collects data by fair and lawful means | Collection methods documentation |
| P4.3 | Collects personal information for current purposes | Purpose documentation, retention limits |
| P5.1 | Use, retention, disposal per policy | Data lifecycle procedures |
| P5.2 | Retains personal information per policy | Retention schedule, disposal records |
| P6.1 | Discloses personal information per policy | Disclosure procedures, third-party agreements |
| P6.2 | Records personal information disclosures | Disclosure logs |
| P6.3 | Creates/retains record of authorized disclosures | Authorization records |
| P6.4 | Obtains privacy commitments from vendors | Vendor DPAs, privacy requirements |
| P6.5 | Obtains privacy commitment compliance evidence | Vendor audits, compliance certifications |
| P6.6 | Notifies affected parties of disclosures | Breach notification procedures |
| P6.7 | Provides notification of privacy incidents | Incident notification procedures |
| P7.1 | Provides data quality mechanisms | Data accuracy procedures, correction mechanisms |
| P8.1 | Complaints and disputes resolution | Complaint handling procedures, escalation process |

---

## Criteria Count Summary
- **CC (Security)**: 33 criteria
- **A (Availability)**: 3 criteria
- **PI (Processing Integrity)**: 5 criteria
- **C (Confidentiality)**: 2 criteria
- **P (Privacy)**: 18 criteria
- **Total**: 61 criteria
