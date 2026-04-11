# Ecosystem Connector Reference — Auto-Evidence Collection

This reference maps **SaaS tools → API endpoints → evidence types → NIST 800-53 controls**. Each control then cascades to 87 frameworks via OSA (`osa_connector.md`).

## Evidence Classification

Every piece of evidence is classified by type and weight:

### Evidence Types
| Type | Code | Description |
|------|------|-------------|
| **Configuration** | `CONFIG` | System settings proving a control exists (e.g., MFA enabled) |
| **Report/Export** | `REPORT` | System-generated data exports (e.g., user list, scan results) |
| **Log** | `LOG` | Timestamped activity records (e.g., access logs, audit trails) |
| **Policy Document** | `POLICY` | Written policies, procedures, and standards |
| **Attestation** | `ATTEST` | Signed acknowledgments, certifications, and declarations |
| **Screenshot** | `SCREEN` | Point-in-time visual proof of a configuration |
| **Test Result** | `TEST` | Outputs of tests (pen test, DR test, backup restore test) |

### Evidence Strength
| Strength | Symbol | When to assign |
|----------|--------|----------------|
| **Primary** | `🟢 P` | Directly proves the control operates effectively. System-generated, tamper-resistant. |
| **Corroborating** | `🔵 C` | Supports or validates primary evidence. Second source confirming same control. |
| **Supplementary** | `⚪ S` | Adds context but cannot stand alone. Policies, training slides, org charts. |

### Auditor Rules
- Every control needs **at least 1 Primary** evidence
- **Primary + Corroborating** = strong (auditor satisfied)
- **Primary alone** = acceptable (auditor may probe)
- **Corroborating alone** = insufficient (auditor will flag)
- **Supplementary alone** = gap (control not evidenced)

### IPE (Information Produced by the Entity) Validation
When evidence comes from the organization's own systems (most API-fetched evidence is IPE):
1. Verify **completeness** — no records filtered out
2. Verify **accuracy** — data matches authoritative source
3. Cross-reference with a **second independent source** when possible
4. Note the **extraction timestamp** for audit trail

---

## Ecosystem Discovery Questionnaire

At the start of an audit, present this questionnaire to identify the organization's tool ecosystem:

```
Which tools does your organization use? (Select all that apply)

IDENTITY & ACCESS MANAGEMENT
□ Okta          □ Microsoft Entra ID (Azure AD)    □ Google Workspace
□ JumpCloud     □ OneLogin    □ Auth0/Okta CIC     □ Ping Identity
□ CyberArk      □ SailPoint   □ Other: _________

HR & PEOPLE
□ BambooHR      □ Workday     □ Gusto       □ Rippling
□ ADP           □ Personio    □ HiBob       □ Other: _________

CLOUD INFRASTRUCTURE
□ AWS           □ Google Cloud (GCP)    □ Microsoft Azure
□ DigitalOcean  □ Oracle Cloud          □ Other: _________

SOURCE CODE & DEVOPS
□ GitHub        □ GitLab      □ Bitbucket    □ Azure DevOps
□ Jenkins       □ CircleCI    □ ArgoCD       □ Other: _________

ENDPOINT & DEVICE MANAGEMENT
□ Jamf          □ Microsoft Intune    □ Kandji    □ Mosyle
□ Workspace ONE □ Other: _________

SECURITY & DETECTION
□ CrowdStrike   □ SentinelOne    □ Carbon Black    □ Microsoft Defender
□ Sophos        □ Palo Alto Cortex XDR              □ Other: _________

VULNERABILITY MANAGEMENT
□ Snyk          □ Qualys      □ Tenable Nessus    □ Rapid7
□ Wiz           □ Orca        □ Checkmarx         □ Other: _________

MONITORING & SIEM
□ Datadog       □ Splunk      □ Elastic/ELK    □ Sumo Logic
□ New Relic     □ Grafana     □ Other: _________

INCIDENT & ON-CALL
□ PagerDuty     □ Opsgenie    □ Rootly    □ FireHydrant
□ Other: _________

TICKETING & PROJECT MANAGEMENT
□ Jira          □ Linear      □ ServiceNow    □ Asana
□ Monday.com    □ ClickUp     □ Other: _________

COMMUNICATION
□ Slack         □ Microsoft Teams    □ Google Chat
□ Zoom          □ Other: _________

PASSWORD & SECRETS
□ 1Password     □ Bitwarden   □ HashiCorp Vault    □ AWS Secrets Manager
□ Doppler       □ Other: _________

BACKUP & DISASTER RECOVERY
□ Veeam         □ AWS Backup    □ Acronis    □ Commvault
□ Druva         □ Other: _________

NETWORK & PERIMETER
□ Cloudflare    □ Zscaler     □ Palo Alto NGFW    □ Fortinet
□ Akamai        □ Other: _________

EMAIL SECURITY
□ Proofpoint    □ Mimecast    □ Google Workspace Security
□ Microsoft Defender for O365  □ Other: _________

TRAINING & AWARENESS
□ KnowBe4       □ Proofpoint SAT    □ Curricula    □ Hoxhunt
□ Other: _________

VENDOR / THIRD-PARTY RISK
□ SecurityScorecard    □ BitSight    □ OneTrust    □ Prevalent
□ Other: _________

DATA LOSS PREVENTION
□ Nightfall     □ Forcepoint    □ Symantec DLP    □ Microsoft Purview
□ Other: _________

COMPLIANCE PLATFORMS (existing)
□ Vanta         □ Drata       □ Secureframe    □ Sprinto
□ Thoropass     □ Other: _________
```

---

## Tool → Evidence → NIST 800-53 Mapping

### Authentication Guide

For each tool, the agent will prompt:

```
"To fetch evidence from [Tool], I need API access.
→ Go to [URL] → Generate a READ-ONLY API key
→ Paste it here (I'll use it in this session only; never stored)"
```

For CLI tools (aws, gcloud, az, kubectl, m365, gws):
```
"I detected [CLI] is installed. Checking authentication..."
→ If authenticated: proceed
→ If not: guide user through auth flow
```

---

## 1. Identity & Access Management

### Okta

**Auth**: `API Token` → Admin Console → Security → API → Create Token (Read-Only Admin)

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /api/v1/users?filter=status eq "ACTIVE"` | Active user inventory | REPORT | 🟢 P | AC-02 (Account Management) |
| `GET /api/v1/users?filter=status eq "ACTIVE"` + check `credentials.provider` for MFA | MFA enrollment status per user | REPORT | 🟢 P | IA-02 (User Identification & Authentication) |
| `GET /api/v1/policies?type=PASSWORD` | Password policy configuration | CONFIG | 🟢 P | IA-05 (Authenticator Management) |
| `GET /api/v1/policies?type=OKTA_SIGN_ON` | Sign-on policy (MFA rules, session timeouts) | CONFIG | 🟢 P | AC-11 (Session Lock), AC-12 (Session Termination) |
| `GET /api/v1/apps` | SSO-enabled application inventory | REPORT | 🟢 P | AC-03 (Access Enforcement) |
| `GET /api/v1/logs?filter=eventType eq "user.lifecycle.deactivate"` | Deprovisioning audit trail | LOG | 🟢 P | PS-04 (Personnel Termination) |
| `GET /api/v1/logs?filter=eventType eq "user.session.start"` | Authentication event logs | LOG | 🔵 C | AU-02 (Auditable Events), AU-12 (Audit Record Generation) |
| `GET /api/v1/logs?filter=eventType eq "user.account.lock"` | Failed login lockout events | LOG | 🔵 C | AC-07 (Unsuccessful Login Attempts) |
| `GET /api/v1/groups` | Group/role membership (RBAC evidence) | REPORT | 🔵 C | AC-03 (Access Enforcement), AC-06 (Least Privilege) |
| `GET /api/v1/users/{userId}/roles` | Admin role assignments | REPORT | 🟢 P | AC-05 (Separation of Duties), AC-06 (Least Privilege) |

### Microsoft Entra ID (Azure AD)

**Auth**: `CLI` → `az login` or `m365 login`

| API / CLI Command | Evidence | Type | Strength | NIST 800-53 |
|-------------------|----------|------|----------|-------------|
| `az ad user list --query "[].{name:displayName,upn:userPrincipalName,enabled:accountEnabled}"` | User directory with status | REPORT | 🟢 P | AC-02 |
| `az ad user list --query "[?accountEnabled==\`true\`]" \| filter for MFA` | MFA enrollment status | REPORT | 🟢 P | IA-02 |
| `m365 entra pim role assignment list` | Privileged access assignments | REPORT | 🟢 P | AC-06 (Least Privilege) |
| MS Graph: `GET /policies/authenticationMethodsPolicy` | Authentication method policies | CONFIG | 🟢 P | IA-05 |
| MS Graph: `GET /identity/conditionalAccess/policies` | Conditional access policies | CONFIG | 🟢 P | AC-03, AC-17 (Remote Access) |
| `m365 entra group list` | Group memberships (RBAC) | REPORT | 🔵 C | AC-03, AC-06 |
| MS Graph: `GET /auditLogs/signIns` | Sign-in audit logs | LOG | 🔵 C | AU-02, AU-12 |

### Google Workspace

**Auth**: `CLI` → `gws auth login -s admin,directory`

| CLI / API | Evidence | Type | Strength | NIST 800-53 |
|-----------|----------|------|----------|-------------|
| `gws admin users list` | Full user directory | REPORT | 🟢 P | AC-02 |
| `gws admin users get --userKey {email}` + 2SV status | MFA enrollment per user | REPORT | 🟢 P | IA-02 |
| Admin API: `GET /admin/directory/v1/users` + `isEnrolledIn2Sv` | Organization-wide MFA report | REPORT | 🟢 P | IA-02 |
| Admin Console: Security → Authentication → 2-Step Verification | 2FA enforcement policy | CONFIG | 🟢 P | IA-05 |
| Admin Console: Security → Password management | Password policy settings | CONFIG | 🔵 C | IA-05 |
| Reports API: `GET /admin/reports/v1/activity/users/admin/login` | Login activity logs | LOG | 🔵 C | AU-02, AU-12 |

---

## 2. HR & People Systems

### BambooHR

**Auth**: `API Key` → Account → API Keys → Add New Key

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /api/gateway.php/{company}/v1/employees/directory` | Employee directory with status | REPORT | 🟢 P | PS-01 (Personnel Security Policy) |
| `GET /api/gateway.php/{company}/v1/employees/changed?since={date}` | New hires & terminations since date | REPORT | 🟢 P | PS-04 (Personnel Termination), PS-05 (Personnel Transfer) |
| `GET /api/gateway.php/{company}/v1/employees/{id}?fields=hireDate,terminationDate,status` | Individual employee lifecycle | REPORT | 🔵 C | PS-04, PS-05 |
| `GET /api/gateway.php/{company}/v1/training/records` | Training completion records | REPORT | 🟢 P | AT-02 (Security Awareness), AT-03 (Security Training) |
| `GET /api/gateway.php/{company}/v1/training/categories` | Training program catalog | REPORT | 🔵 C | AT-01 (Training Policy & Procedures) |
| Cross-reference: employee directory vs. Okta/Entra user list | Orphaned accounts detection | TEST | 🟢 P | AC-02 (Account Management) |

### Workday

**Auth**: `API Credentials` → Integration → API Client

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /ccx/api/v1/{tenant}/workers` | Worker directory | REPORT | 🟢 P | PS-01 |
| `GET /ccx/api/v1/{tenant}/workers?terminationDate>={date}` | Terminated workers | REPORT | 🟢 P | PS-04 |
| Workday Learning: completion reports | Training records | REPORT | 🟢 P | AT-02, AT-03, AT-04 (Training Records) |
| `GET /ccx/api/v1/{tenant}/workers` + position/role data | Position descriptions & risk categorization | REPORT | 🔵 C | PS-02 (Position Categorization), PS-09 (Position Descriptions) |

---

## 3. Cloud Infrastructure

### AWS

**Auth**: `CLI` → `aws configure` or SSO → `aws sso login`

| CLI Command | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `aws iam get-account-summary` | IAM account summary (MFA, users, policies) | REPORT | 🟢 P | AC-02, IA-02 |
| `aws iam generate-credential-report && aws iam get-credential-report` | Full credential report (password age, MFA, access keys) | REPORT | 🟢 P | IA-05, AC-02 |
| `aws iam list-users \| aws iam list-mfa-devices` | MFA status per user | REPORT | 🟢 P | IA-02 |
| `aws iam list-attached-user-policies --user-name {user}` | Per-user IAM policies | REPORT | 🟢 P | AC-03, AC-06 |
| `aws organizations list-accounts` | Account inventory | REPORT | 🟢 P | CM-08 (Component Inventory) |
| `aws ec2 describe-instances` | Compute asset inventory | REPORT | 🟢 P | CM-08 |
| `aws rds describe-db-instances --query "DBInstances[].{id:DBInstanceIdentifier,encrypted:StorageEncrypted}"` | RDS encryption status | CONFIG | 🟢 P | SC-28 (Protection of Information at Rest) |
| `aws s3api get-bucket-encryption --bucket {name}` | S3 encryption configuration | CONFIG | 🟢 P | SC-28 |
| `aws s3api get-public-access-block --bucket {name}` | S3 public access block | CONFIG | 🟢 P | AC-22 (Publicly Accessible Content) |
| `aws cloudtrail describe-trails` | CloudTrail logging configuration | CONFIG | 🟢 P | AU-02, AU-03 (Content of Audit Records) |
| `aws cloudtrail get-trail-status --name {trail}` | CloudTrail operational status | CONFIG | 🔵 C | AU-06 (Audit Monitoring) |
| `aws logs describe-log-groups` | CloudWatch log retention | CONFIG | 🟢 P | AU-11 (Audit Record Retention) |
| `aws ec2 describe-security-groups` | Security group rules (firewall) | CONFIG | 🟢 P | SC-07 (Boundary Protection) |
| `aws ec2 describe-vpcs` | VPC network architecture | CONFIG | 🔵 C | SC-07 |
| `aws ec2 describe-flow-logs` | VPC Flow Log configuration | CONFIG | 🟢 P | AU-12 |
| `aws backup list-backup-plans` | Backup plan configuration | CONFIG | 🟢 P | CP-09 (Information System Backup) |
| `aws backup list-recovery-points-by-backup-vault --backup-vault-name {name}` | Backup completion records | REPORT | 🔵 C | CP-09 |
| `aws guardduty list-detectors` | Threat detection status | CONFIG | 🟢 P | SI-04 (System Monitoring) |
| `aws inspector2 list-findings --filter-criteria '{"findingStatus":[{"comparison":"EQUALS","value":"ACTIVE"}]}'` | Active vulnerability findings | REPORT | 🟢 P | RA-05 (Vulnerability Scanning), SI-02 (Flaw Remediation) |
| `aws kms list-keys` | Encryption key inventory | REPORT | 🟢 P | SC-12 (Cryptographic Key Management) |
| `aws kms describe-key --key-id {id}` | Key rotation policy | CONFIG | 🔵 C | SC-12 |
| `aws securityhub get-findings` | Security Hub aggregated findings | REPORT | 🔵 C | RA-05, SI-04 |
| `aws config describe-compliance-by-config-rule` | AWS Config compliance status | REPORT | 🔵 C | CM-06 (Configuration Settings), CA-07 (Continuous Monitoring) |

### Google Cloud (GCP)

**Auth**: `CLI` → `gcloud auth login`

| CLI Command | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `gcloud iam service-accounts list` | Service account inventory | REPORT | 🟢 P | AC-02 |
| `gcloud projects get-iam-policy {project}` | IAM policy bindings | REPORT | 🟢 P | AC-03, AC-06 |
| `gcloud compute instances list` | Compute asset inventory | REPORT | 🟢 P | CM-08 |
| `gcloud compute firewall-rules list` | Firewall rules | CONFIG | 🟢 P | SC-07 |
| `gcloud sql instances list --format="table(name,settings.ipConfiguration.requireSsl,settings.dataDiskType)"` | Cloud SQL encryption & SSL | CONFIG | 🟢 P | SC-08 (Transmission Integrity), SC-28 |
| `gcloud logging sinks list` | Logging sink configuration | CONFIG | 🟢 P | AU-02, AU-12 |
| `gcloud kms keys list --location={loc} --keyring={ring}` | KMS key inventory | REPORT | 🟢 P | SC-12 |
| `gcloud scc findings list {org-id}` | Security Command Center findings | REPORT | 🔵 C | SI-04, RA-05 |

### Microsoft Azure

**Auth**: `CLI` → `az login`

| CLI Command | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `az vm list --query "[].{name:name,rg:resourceGroup,size:hardwareProfile.vmSize}"` | VM inventory | REPORT | 🟢 P | CM-08 |
| `az network nsg list` | Network security groups | CONFIG | 🟢 P | SC-07 |
| `az storage account list --query "[].{name:name,encryption:encryption.services}"` | Storage encryption status | CONFIG | 🟢 P | SC-28 |
| `az keyvault list` | Key Vault inventory | REPORT | 🟢 P | SC-12 |
| `az monitor log-analytics workspace list` | Log Analytics configuration | CONFIG | 🟢 P | AU-02, AU-06 |
| `az security assessment list` | Microsoft Defender findings | REPORT | 🔵 C | RA-05, SI-04 |
| `az backup policy list --vault-name {name} --resource-group {rg}` | Backup policies | CONFIG | 🟢 P | CP-09 |

---

## 4. Source Code & DevOps

### GitHub

**Auth**: `Personal Access Token` → Settings → Developer Settings → Fine-grained Tokens (read-only)

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /repos/{owner}/{repo}/branches/{branch}/protection` | Branch protection rules | CONFIG | 🟢 P | CM-05 (Access Restrictions for Change) |
| `GET /repos/{owner}/{repo}/rulesets` | Repository rulesets | CONFIG | 🟢 P | CM-03 (Configuration Change Control) |
| `GET /repos/{owner}/{repo}/pulls?state=closed&per_page=50` | Merged PR history (code review evidence) | LOG | 🟢 P | SA-11 (Developer Security Testing) |
| `GET /repos/{owner}/{repo}/code-scanning/alerts` | Code scanning (SAST) results | REPORT | 🟢 P | SA-11, RA-05 |
| `GET /repos/{owner}/{repo}/dependabot/alerts` | Dependency vulnerability alerts | REPORT | 🟢 P | RA-05, SI-02, SR-03 (Supply Chain Controls) |
| `GET /repos/{owner}/{repo}/secret-scanning/alerts` | Secret scanning alerts | REPORT | 🟢 P | IA-05, SC-28 |
| `GET /repos/{owner}/{repo}/actions/runs` | CI/CD pipeline execution logs | LOG | 🔵 C | SA-10 (Developer Configuration Management) |
| `GET /orgs/{org}/members` | Organization member list | REPORT | 🔵 C | AC-02 |
| `GET /orgs/{org}/teams` | Team structure (RBAC) | REPORT | 🔵 C | AC-06 |
| `GET /repos/{owner}/{repo}/commits?since={date}` | Commit audit trail | LOG | 🔵 C | CM-03, AU-12 |

### GitLab

**Auth**: `Personal Access Token` → Preferences → Access Tokens (read_api scope)

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /projects/{id}/protected_branches` | Branch protection config | CONFIG | 🟢 P | CM-05 |
| `GET /projects/{id}/merge_requests?state=merged` | Merged MR history | LOG | 🟢 P | SA-11 |
| `GET /projects/{id}/vulnerability_findings` | SAST/DAST findings | REPORT | 🟢 P | RA-05, SA-11 |
| `GET /projects/{id}/pipelines` | CI/CD pipeline logs | LOG | 🔵 C | SA-10 |

---

## 5. Endpoint & Device Management

### Jamf Pro

**Auth**: `API Credentials` → Settings → API Roles & Clients

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /api/v1/computers-inventory` | Managed device inventory | REPORT | 🟢 P | CM-08 |
| `GET /api/v1/computers-inventory` + check `osVersion` | OS patch level per device | REPORT | 🟢 P | SI-02 (Flaw Remediation) |
| `GET /api/v1/computers-inventory` + check `diskEncryption` | FileVault encryption status | REPORT | 🟢 P | SC-28, MP-04 (Media Storage) |
| `GET /api/v1/compliance-policies` | MDM compliance policies | CONFIG | 🟢 P | CM-06 (Configuration Settings) |
| `GET /api/v1/computer-prestages` | Auto-enrollment config | CONFIG | 🔵 C | CM-02 (Baseline Configuration) |

### Microsoft Intune

**Auth**: `CLI` → `m365 login` or MS Graph API

| API / CLI | Evidence | Type | Strength | NIST 800-53 |
|-----------|----------|------|----------|-------------|
| MS Graph: `GET /deviceManagement/managedDevices` | Managed device inventory | REPORT | 🟢 P | CM-08 |
| MS Graph: `GET /deviceManagement/deviceCompliancePolicies` | Compliance policy configs | CONFIG | 🟢 P | CM-06 |
| MS Graph: `GET /deviceManagement/managedDevices` + `isEncrypted` | Encryption status | REPORT | 🟢 P | SC-28 |
| MS Graph: `GET /deviceManagement/managedDevices` + `osVersion` | Patch compliance | REPORT | 🟢 P | SI-02 |

---

## 6. Security & Detection (EDR/XDR)

### CrowdStrike Falcon

**Auth**: `API Client` → Support → API Clients → Add Client (Read scope)

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /devices/queries/devices/v1` + `GET /devices/entities/devices/v2` | Endpoint inventory with agent status | REPORT | 🟢 P | CM-08, SI-03 (Malicious Code Protection) |
| `GET /policy/queries/prevention/v1` | Prevention policies | CONFIG | 🟢 P | SI-03, SI-04 |
| `GET /detects/queries/detects/v1` | Detection/incident feed | LOG | 🟢 P | IR-04 (Incident Handling), IR-05 (Incident Monitoring) |
| `GET /intel/queries/vulnerabilities/v1` | Vulnerability assessments | REPORT | 🔵 C | RA-05 |

### SentinelOne

**Auth**: `API Token` → Settings → Users → API Token

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /web/api/v2.1/agents` | Agent inventory and health | REPORT | 🟢 P | CM-08, SI-03 |
| `GET /web/api/v2.1/policies` | Security policies | CONFIG | 🟢 P | SI-03, SI-04 |
| `GET /web/api/v2.1/threats` | Detected threats | LOG | 🟢 P | IR-04, IR-05 |

---

## 7. Vulnerability Management

### Snyk

**Auth**: `API Token` → Account Settings → API Token

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /org/{orgId}/projects` | Monitored project inventory | REPORT | 🟢 P | CM-08, RA-05 |
| `GET /org/{orgId}/project/{projectId}/issues` | Vulnerability findings per project | REPORT | 🟢 P | RA-05, SI-02 |
| `GET /org/{orgId}/project/{projectId}/dep-graph` | Dependency graph (supply chain) | REPORT | 🟢 P | SR-03 (Supply Chain Controls), SR-04 (Provenance) |
| `GET /org/{orgId}/audit-logs` | Audit log trail | LOG | 🔵 C | AU-02, AU-12 |

### Qualys / Tenable / Rapid7

**Auth**: `API Credentials` — varies by platform

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| Vulnerability scan results (all hosts) | REPORT | 🟢 P | RA-05 |
| Remediation SLA configuration | CONFIG | 🟢 P | SI-02 |
| Scan schedule/automation proof | CONFIG | 🔵 C | RA-05 |
| Trend report (remediation velocity) | REPORT | 🔵 C | CA-05 (Plan of Action & Milestones) |

---

## 8. Monitoring & SIEM

### Datadog

**Auth**: `API Key + Application Key` → Organization Settings → API Keys

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /api/v1/monitor` | Alert/monitor configurations | CONFIG | 🟢 P | SI-04 (System Monitoring), AU-06 |
| `GET /api/v2/logs/events/search` | Log search (retention proof) | LOG | 🟢 P | AU-11 (Audit Record Retention) |
| `GET /api/v1/dashboard/lists/manual` | Security dashboards | CONFIG | 🔵 C | SI-04, AU-06 |
| `GET /api/v2/security_monitoring/rules` | Security monitoring rules (SIEM) | CONFIG | 🟢 P | SI-04, AU-06 |

### Splunk

**Auth**: `API Token` → Settings → Tokens

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /services/saved/searches` | Saved searches / correlation rules | CONFIG | 🟢 P | SI-04, AU-06 |
| `GET /services/data/indexes` | Index retention policies | CONFIG | 🟢 P | AU-11 |
| `POST /services/search/jobs` → query notable events | Notable events (incidents) | LOG | 🟢 P | IR-04, IR-05 |

### PagerDuty

**Auth**: `API Key` → User Settings → API Access → Create API Key

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /escalation_policies` | Escalation policies (incident response chain) | CONFIG | 🟢 P | IR-01 (Incident Response Plan), IR-07 (Incident Response Assistance) |
| `GET /schedules` | On-call schedules | CONFIG | 🔵 C | IR-01 |
| `GET /incidents?since={date}&until={date}` | Incident history with resolution times | LOG | 🟢 P | IR-04, IR-05, IR-06 (Incident Reporting) |

---

## 9. Ticketing & Project Management

### Jira

**Auth**: `API Token` → Atlassian Account → Security → API Tokens

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /rest/api/3/search?jql=project={project} AND type=Bug AND labels=security` | Security bug tracking | LOG | 🟢 P | SI-02, CA-05 |
| `GET /rest/api/3/search?jql=type="Change Request"` | Change management tickets | LOG | 🟢 P | CM-03 |
| `GET /rest/api/3/search?jql=type="Incident"` | Incident tickets | LOG | 🟢 P | IR-04, IR-05 |
| `GET /rest/api/3/workflow` | Workflow configurations (approval gates) | CONFIG | 🔵 C | CM-03 |

### ServiceNow

**Auth**: `API Credentials` → System Admin → OAuth → Application Registry

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /api/now/table/incident` | Incident records | LOG | 🟢 P | IR-04, IR-05 |
| `GET /api/now/table/change_request` | Change requests with approvals | LOG | 🟢 P | CM-03, CM-05 |
| `GET /api/now/table/cmdb_ci` | Configuration item inventory (CMDB) | REPORT | 🟢 P | CM-08 |
| `GET /api/now/table/sys_user` | User directory | REPORT | 🔵 C | AC-02 |

---

## 10. Password & Secrets Management

### 1Password Business

**Auth**: `API Token` → 1Password.com → Integrations → Directory → SCIM Bridge or Events API

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| Events API: `POST /api/v1/signinattempts` | Sign-in attempts | LOG | 🔵 C | AC-07, AU-02 |
| Events API: `POST /api/v1/auditevents` | Vault access audit trail | LOG | 🟢 P | AU-02, AU-12 |
| Admin Console: Team policies | Password & vault policies | CONFIG | 🟢 P | IA-05 |

### HashiCorp Vault

**Auth**: `Vault Token` → `vault token create -policy=audit-read`

| CLI / API | Evidence | Type | Strength | NIST 800-53 |
|-----------|----------|------|----------|-------------|
| `vault secrets list` | Secrets engine inventory | REPORT | 🟢 P | SC-12, IA-05 |
| `vault audit list` | Audit device configuration | CONFIG | 🟢 P | AU-02, AU-12 |
| `vault read sys/policies/acl/{policy}` | Access policies | CONFIG | 🟢 P | AC-03, AC-06 |
| `vault read sys/rotate/config` | Key rotation policy | CONFIG | 🟢 P | SC-12 |

---

## 11. Backup & Disaster Recovery

### Veeam / AWS Backup / Acronis

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| Backup schedule configuration | CONFIG | 🟢 P | CP-09 (Information System Backup) |
| Backup job completion reports (last 90 days) | REPORT | 🟢 P | CP-09 |
| Restore test results | TEST | 🟢 P | CP-04 (Contingency Plan Testing), CP-10 (System Recovery) |
| RPO/RTO configuration | CONFIG | 🔵 C | CP-02 (Contingency Plan) |
| DR test report / tabletop exercise notes | TEST | 🟢 P | CP-04 |
| Offsite/cross-region replication config | CONFIG | 🔵 C | CP-06 (Alternate Storage Site), CP-07 (Alternate Processing Site) |

---

## 12. Network & Perimeter Security

### Cloudflare

**Auth**: `API Token` → My Profile → API Tokens → Create Token

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /zones/{zone}/firewall/rules` | WAF rules | CONFIG | 🟢 P | SC-07 |
| `GET /zones/{zone}/settings/ssl` | TLS/SSL configuration | CONFIG | 🟢 P | SC-08, SC-13 (Use of Cryptography) |
| `GET /zones/{zone}/dns_records` + check DMARC/DKIM/SPF | Email security DNS records | CONFIG | 🟢 P | SI-08 (Spam Protection) |
| `GET /zones/{zone}/settings/security_level` | DDoS protection level | CONFIG | 🟢 P | SC-05 (Denial of Service Protection) |
| `GET /zones/{zone}/analytics/dashboard` | Traffic analytics | REPORT | 🔵 C | SI-04 |

---

## 13. Email Security

### Google Workspace / Microsoft 365

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| DMARC policy record (`_dmarc.domain.com TXT`) | CONFIG | 🟢 P | SI-08 |
| DKIM signing configuration | CONFIG | 🟢 P | SI-08 |
| SPF record | CONFIG | 🔵 C | SI-08 |
| Email filtering/quarantine policy | CONFIG | 🟢 P | SI-08, SI-03 |
| Email retention policy | CONFIG | 🔵 C | AU-11 |
| DLP policy for email | CONFIG | 🟢 P | AC-04 (Information Flow Enforcement) |

---

## 14. Training & Security Awareness

### KnowBe4

**Auth**: `API Key` → Account Settings → API

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `GET /v1/training/enrollments` | Training enrollment & completion | REPORT | 🟢 P | AT-02 (Security Awareness), AT-04 (Training Records) |
| `GET /v1/phishing/campaigns` | Phishing simulation campaign results | TEST | 🟢 P | AT-02 |
| `GET /v1/users` | User training status | REPORT | 🔵 C | AT-03 (Security Training) |
| `GET /v1/phishing/campaigns/{id}/results` | Click rate & report rate per campaign | TEST | 🔵 C | AT-02 |

---

## 15. Vendor & Third-Party Risk

### SecurityScorecard / BitSight

**Auth**: `API Key` from vendor portal

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| Vendor security rating scorecards | REPORT | 🟢 P | SA-09 (External Information System Services), SR-06 (Supplier Assessments) |
| Continuous monitoring alerts for vendors | LOG | 🟢 P | PM-30 (Supply Chain Risk Management), SR-06 |
| Vendor security questionnaire responses | ATTEST | 🔵 C | SA-09, SR-06 |
| Vendor SOC 2 / ISO 27001 certificates | ATTEST | 🟢 P | SA-09 |
| Fourth-party risk assessments | REPORT | 🔵 C | SR-03 |

---

## 16. Data Loss Prevention

### Nightfall / Microsoft Purview / Forcepoint

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| DLP policy configuration | CONFIG | 🟢 P | AC-04 (Information Flow Enforcement), SC-07 |
| DLP incident/violation reports | LOG | 🟢 P | AC-04, SI-04 |
| Data classification schema | POLICY | 🟢 P | RA-02 (Security Categorization) |
| Sensitive data discovery scan results | REPORT | 🟢 P | CM-12 (Information Location) |

---

## 17. Communication & Collaboration

### Slack

**Auth**: `API Token` → Admin → Manage Apps → build app with `admin.*` scopes

| API Endpoint | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| Admin API: `GET /admin.conversations.getTeams` | Workspace inventory | REPORT | 🔵 C | CM-08 |
| Admin API: workspace retention policies | Message retention configuration | CONFIG | 🟢 P | AU-11, SI-12 (Information Output Handling) |
| Admin API: `GET /admin.users.list` | User directory with roles | REPORT | 🔵 C | AC-02 |
| Enterprise Grid: DLP integration config | DLP policy status | CONFIG | 🔵 C | AC-04 |

---

## 18. Compliance Platforms (Existing Evidence Import)

### Vanta / Drata / Secureframe / Sprinto

If the organization already uses a compliance platform, **import their existing evidence**:

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| Control status dashboard export | REPORT | 🟢 P | CA-07 (Continuous Monitoring) |
| Automated test results per control | TEST | 🟢 P | (varies by control) |
| Policy document library | POLICY | ⚪ S | (varies) |
| Remediation task board | REPORT | 🔵 C | CA-05 (Plan of Action & Milestones) |
| Audit trail / changelog | LOG | 🔵 C | AU-02, AU-12 |

---

## 19. Physical Security

### Verkada / Brivo / Openpath

| Evidence Type | Type | Strength | NIST 800-53 |
|--------------|------|----------|-------------|
| Badge reader access logs | LOG | 🟢 P | PE-03 (Physical Access Control), PE-08 (Access Records) |
| Visitor management records | LOG | 🟢 P | PE-07 (Visitor Control) |
| Camera retention policy | CONFIG | 🟢 P | PE-06 (Monitoring Physical Access) |
| Physical access authorization list | REPORT | 🟢 P | PE-02 (Physical Access Authorizations) |

---

## 20. Container & Kubernetes

### Kubernetes / EKS / GKE / AKS

**Auth**: `kubectl` with appropriate kubeconfig

| CLI Command | Evidence | Type | Strength | NIST 800-53 |
|-------------|----------|------|----------|-------------|
| `kubectl get pods --all-namespaces` | Running workload inventory | REPORT | 🟢 P | CM-08 |
| `kubectl get networkpolicies --all-namespaces` | Network policies | CONFIG | 🟢 P | SC-07, AC-04 |
| `kubectl get podsecuritypolicies` or `kubectl get constraints` (OPA/Gatekeeper) | Pod security policies | CONFIG | 🟢 P | CM-06, SC-39 (Process Isolation) |
| `kubectl get clusterrolebindings` | RBAC bindings | CONFIG | 🟢 P | AC-03, AC-06 |
| Container image scanning results (Trivy, Snyk Container) | Image vulnerability report | REPORT | 🟢 P | RA-05, SI-02 |

---

## Cross-Reference Evidence Table

When running an audit, cross-reference evidence sources to strengthen findings:

| Cross-Reference | What It Proves | NIST 800-53 |
|-----------------|---------------|-------------|
| HR directory ↔ IAM user list | No orphaned accounts (terminated employees still with access) | AC-02, PS-04 |
| IAM users ↔ MFA report | 100% MFA coverage | IA-02 |
| Vulnerability scan ↔ Ticket system | Vulnerabilities are tracked and remediated | RA-05, SI-02 |
| Backup schedule ↔ Restore test logs | Backups are tested and recoverable | CP-09, CP-04 |
| Code review policy ↔ Merged PR history | Code reviews are actually enforced | SA-11, CM-05 |
| Training records ↔ Employee directory | All employees completed training | AT-02, AT-03 |
| Endpoint inventory ↔ MDM compliance | All devices meet security baseline | CM-06, CM-08 |
| Incident tickets ↔ PagerDuty history | Incidents are properly logged and escalated | IR-04, IR-05 |

---

## Attribution

```
NIST 800-53 Rev 5 control mappings in this document reference the
Open Security Architecture (opensecurityarchitecture.org) control catalog.
Licensed under CC BY-SA 4.0.
```
