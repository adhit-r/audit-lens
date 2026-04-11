# EU AI Act — Compliance Reference

The European Union's AI Act is a risk-based regulatory framework governing the development, deployment, and use of AI systems within the EU. It classifies AI systems into risk tiers and imposes obligations proportional to the risk level.

## Risk Classification

### Step 1: Determine if the AI system is prohibited (Unacceptable Risk)

The following AI practices are **banned outright** (Article 5):

| Prohibited Practice | Description |
|---------------------|-------------|
| Social scoring | AI systems used by public authorities to evaluate trustworthiness based on social behavior or personal characteristics |
| Real-time biometric identification | Remote biometric identification in public spaces for law enforcement (narrow exceptions) |
| Subliminal manipulation | AI designed to manipulate behavior beyond a person's consciousness causing harm |
| Exploitation of vulnerabilities | AI targeting specific groups (children, disabled, elderly) to exploit their vulnerabilities |
| Biometric categorization | Inferring sensitive attributes (race, political opinions, sexual orientation) from biometric data |
| Facial recognition databases | Untargeted scraping of facial images from the internet or CCTV for facial recognition databases |
| Emotion recognition | In workplaces and educational institutions (with limited exceptions) |
| Predictive policing | Individual-level risk assessments based solely on profiling or personality traits |

**If the system falls under any prohibited practice → flag immediately and recommend discontinuation.**

---

### Step 2: Determine if the system is High-Risk

A system is **high-risk** if it falls into one of two categories:

#### Category 1: Safety components of regulated products
AI systems used as safety components of products already covered by EU harmonization legislation:
- Medical devices
- Motor vehicles
- Aviation systems
- Machinery
- Toys
- Lifts
- Radio equipment
- Pressure equipment
- Marine equipment

#### Category 2: Standalone high-risk systems (Annex III)

| Area | Examples |
|------|---------|
| **Biometric identification** | Remote biometric identification, biometric categorization, emotion recognition |
| **Critical infrastructure** | AI managing road traffic, water/gas/heating/electricity supply, digital infrastructure |
| **Education and training** | AI determining access to educational institutions, evaluating learning outcomes, proctoring |
| **Employment** | Recruitment/screening tools, promotion/termination decisions, task allocation, performance monitoring |
| **Essential services** | Credit scoring, insurance risk assessment, emergency services dispatch |
| **Law enforcement** | Risk assessment of individuals, polygraph/deception detection, profiling in criminal investigations |
| **Migration and border** | Risk assessment for irregular migration, visa/asylum application processing |
| **Justice and democracy** | AI assisting judicial authorities, influencing election outcomes |

---

### Step 3: Apply requirements based on classification

## Requirements by Risk Level

### High-Risk Systems — Full Compliance Required

#### For Providers (developers/manufacturers):

| Requirement | Article | Description |
|------------|---------|-------------|
| **Risk Management System** | Art. 9 | Establish and maintain a comprehensive risk management system throughout the entire AI lifecycle. Identify, estimate, evaluate, and mitigate risks. |
| **Data Governance** | Art. 10 | Training, validation, and testing datasets must meet quality criteria: relevant, representative, free of errors, complete. Bias examination required. |
| **Technical Documentation** | Art. 11 | Maintain detailed technical documentation demonstrating compliance. Must be available to regulatory authorities. |
| **Record-Keeping** | Art. 12 | Automatic logging of events during operation to ensure traceability. Logs must enable monitoring of system operation. |
| **Transparency** | Art. 13 | System must be sufficiently transparent to enable deployers to interpret output and use it appropriately. Instructions for use required. |
| **Human Oversight** | Art. 14 | Design systems to allow effective human oversight. Humans must be able to understand capabilities/limitations, monitor operation, and intervene or override. |
| **Accuracy, Robustness, Security** | Art. 15 | Achieve appropriate levels of accuracy, robustness, and cybersecurity throughout lifecycle. Resilience against adversarial attacks. |
| **Quality Management System** | Art. 17 | Implement a QMS covering: compliance strategy, design/development/testing procedures, risk management, post-market monitoring, incident reporting. |
| **Conformity Assessment** | Art. 43 | Undergo conformity assessment before placing on market. Self-assessment for most systems; third-party for biometric identification. |
| **EU Database Registration** | Art. 49 | Register the system in the EU public database before deployment. |
| **Post-Market Monitoring** | Art. 72 | Establish and document a post-market monitoring system proportionate to the risk. |
| **Serious Incident Reporting** | Art. 73 | Report serious incidents to relevant authorities within prescribed timeframes. |

#### For Deployers (organizations using the AI):

| Requirement | Article | Description |
|------------|---------|-------------|
| **Instructions compliance** | Art. 26(1) | Use the AI system in accordance with provider's instructions for use. |
| **Human oversight** | Art. 26(2) | Assign human oversight to competent, trained, and authorized persons. |
| **Input data quality** | Art. 26(4) | Ensure input data is relevant and sufficiently representative for the intended purpose. |
| **Monitoring** | Art. 26(5) | Monitor operation and report malfunctions, incidents, and risks to the provider. |
| **Record retention** | Art. 26(6) | Keep logs generated by the system for at least 6 months unless otherwise required. |
| **DPIA** | Art. 26(9) | Conduct a Data Protection Impact Assessment where required under GDPR. |
| **Fundamental rights assessment** | Art. 27 | Perform an assessment of the impact on fundamental rights before deploying high-risk AI. |

---

### Limited-Risk Systems — Transparency Requirements

| Requirement | Description |
|------------|-------------|
| **AI interaction disclosure** | Inform individuals that they are interacting with an AI system (chatbots, virtual assistants) |
| **Deepfake labeling** | AI-generated or manipulated content (audio, image, video) must be labeled as artificially generated |
| **AI-generated text disclosure** | Text generated by AI for public information purposes must be labeled as AI-generated |
| **Emotion recognition disclosure** | Inform individuals when emotion recognition or biometric categorization is being applied to them |

---

### Minimal-Risk Systems — No Mandatory Requirements

Voluntary codes of conduct encouraged. Examples:
- AI spam filters
- AI-enabled video games
- Inventory management systems
- AI-assisted translation tools

---

## General-Purpose AI (GPAI) Models — Special Rules

| Category | Requirements |
|----------|-------------|
| **All GPAI models** | Technical documentation, training data policies, copyright compliance, publish summary of training data content |
| **GPAI with systemic risk** | All of the above PLUS: model evaluation, adversarial testing, incident tracking and reporting, cybersecurity protections, energy consumption reporting |

Systemic risk is determined by cumulative compute used for training (threshold: 10^25 FLOPs) or by Commission designation.

---

## Enforcement and Penalties

| Violation Category | Maximum Fine |
|-------------------|-------------|
| Prohibited AI practices | €35M or 7% of global annual turnover |
| High-risk system non-compliance | €15M or 3% of global annual turnover |
| Incorrect information to authorities | €7.5M or 1% of global annual turnover |

For SMEs and startups, fines are capped at the lower percentage threshold.

---

## Timeline

| Date | Milestone |
|------|-----------|
| August 2024 | Entry into force |
| February 2025 | Prohibited AI practices apply |
| August 2025 | GPAI model obligations apply |
| August 2026 | High-risk AI system obligations apply (Annex III) |
| August 2027 | High-risk AI as safety components of products apply (Annex I) |

---

## Cross-Reference to ISO 42001

| EU AI Act Requirement | Related ISO 42001 Controls |
|----------------------|---------------------------|
| Risk Management System (Art. 9) | A.5.1 Lifecycle planning, A.6.5 Bias assessment |
| Data Governance (Art. 10) | A.6.1-A.6.7 Data management |
| Technical Documentation (Art. 11) | Clause 7.5 Documented information |
| Transparency (Art. 13) | A.7.1-A.7.5 Information for interested parties |
| Human Oversight (Art. 14) | A.8.3 Human oversight |
| Accuracy/Robustness (Art. 15) | A.5.5 Verification and validation |
| Quality Management (Art. 17) | Clauses 4-10 (full management system) |
| Post-Market Monitoring (Art. 72) | A.5.7 Operation and monitoring, A.8.4 Monitoring |

## Cross-Reference to GDPR

| EU AI Act Requirement | Related GDPR Articles |
|----------------------|----------------------|
| Data Governance (Art. 10) | Art. 5 (Data quality), Art. 25 (Privacy by design) |
| Transparency (Art. 13) | Art. 13-14 (Information to data subjects) |
| Fundamental Rights Assessment (Art. 27) | Art. 35 (DPIA) |
| Record-Keeping (Art. 12) | Art. 30 (Records of processing) |
