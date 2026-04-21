# Data Retention and Disposal Policy

## Document Governance
| Attribute | Detail |
|-----------|--------|
| **Document Owner** | Chief Information Security Officer (CISO) |
| **Classification** | Internal |
| **Version** | 1.0 (Auto-Generated Draft) |
| **Last Updated** | 2026-04-12 |
| **Next Review Due** | 2027-04-12 |

*Generated via AuditLens Remediation Engine*

## 1. Purpose
The purpose of this Data Retention and Disposal Policy is to specify how long Acme Corp must retain data and the procedures for securely destroying data when it is no longer needed.

## 2. Retention Periods
- **Customer Data (AWS S3/RDS)**: Retained for the duration of the active contract + 30 days unless legally required otherwise.
- **Log Data (Datadog/CloudTrail)**: Security and audit logs are retained in immutable storage for a period of 12 months.
- **Employee Records (BambooHR)**: 7 years post-termination.

## 3. Secure Disposal
### 3.1 Digital Media
All digital volumes (EBS) and buckets (S3) must be cryptographically wiped. Acme Corp uses AWS KMS managed keys. Destroying the key constitutes cryptographic erasure.

### 3.2 Physical Hardware
Acme Corp operates a remote-first, cloud-native (AWS) infrastructure and maintains no physical servers. All employee laptops must be securely wiped via our MDM (Kandji) before disposal.
