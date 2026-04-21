# NIST AI Risk Management Framework (AI RMF 1.0) & AI 600-1 GenAI Profile

The NIST AI RMF is a voluntary framework for managing risks associated with AI systems. AI 600-1 extends it specifically for generative AI risks. Unlike ISO 42001 (certifiable standard) or the EU AI Act (regulation), this is guidance-based.

## Core Functions

The framework is organized into four core functions, each with categories and subcategories.

---

### GOVERN — Establish AI governance

Policies, processes, procedures, and practices across the organization related to AI risk management.

| Category | Subcategory | Description |
|----------|-------------|-------------|
| GOVERN 1 | Policies | Organizational policies for AI risk management are established and regularly reviewed. |
| GOVERN 1.1 | Legal compliance | Legal and regulatory requirements involving AI are understood, managed, and documented. |
| GOVERN 1.2 | Trustworthy AI characteristics | Policies reflect the organization's values and principles for trustworthy AI (valid, reliable, safe, secure, resilient, accountable, transparent, explainable, interpretable, privacy-enhanced, fair). |
| GOVERN 1.3 | AI risk management integration | AI risk management is integrated with broader enterprise risk management. |
| GOVERN 1.4 | Ongoing monitoring | Ongoing monitoring and periodic review of AI risk management processes are in place. |
| GOVERN 1.5 | Risk tolerance | Organizational risk tolerance for AI is established and communicated. |
| GOVERN 1.6 | Workforce diversity | Policies foster diversity, equity, inclusion, and accessibility in AI teams. |
| GOVERN 1.7 | AI lifecycle processes | Processes and procedures are in place for all stages of the AI lifecycle. |
| GOVERN 2 | Accountability | Roles, responsibilities, and lines of authority for AI risk management are defined. |
| GOVERN 2.1 | Roles and responsibilities | Clearly defined and documented roles for AI development, deployment, and oversight. |
| GOVERN 2.2 | Training | Personnel are trained on AI risk management responsibilities. |
| GOVERN 2.3 | Executive oversight | Senior leadership is engaged in AI risk management decisions. |
| GOVERN 3 | Workforce | AI workforce has appropriate skills, training, and ongoing development. |
| GOVERN 3.1 | AI literacy | The organization fosters AI literacy across all levels. |
| GOVERN 3.2 | Interdisciplinary teams | AI development involves diverse perspectives including domain experts, social scientists, ethicists. |
| GOVERN 4 | Culture | Organizational culture supports responsible AI practices. |
| GOVERN 4.1 | Risk culture | A culture of risk awareness and open communication about AI risks is fostered. |
| GOVERN 4.2 | Feedback mechanisms | Mechanisms exist for internal and external stakeholders to report AI concerns. |
| GOVERN 5 | Stakeholder engagement | Relevant stakeholders are engaged throughout the AI lifecycle. |
| GOVERN 5.1 | Stakeholder identification | AI stakeholders (internal, external, affected communities) are identified. |
| GOVERN 5.2 | Stakeholder feedback | Stakeholder feedback is collected and incorporated into AI governance. |
| GOVERN 6 | Third-party management | Risks from third-party AI components and services are managed. |
| GOVERN 6.1 | Third-party policies | Policies for using and integrating third-party AI systems are established. |
| GOVERN 6.2 | Supply chain risk | AI supply chain risks (data, models, platforms) are assessed and managed. |

---

### MAP — Context and risk identification

Understanding the context in which AI systems operate and identifying potential risks.

| Category | Subcategory | Description |
|----------|-------------|-------------|
| MAP 1 | Context | The context of use for the AI system is understood and documented. |
| MAP 1.1 | Intended purpose | The intended purpose, use cases, and deployment context are clearly defined. |
| MAP 1.2 | Interdependencies | Technical and societal interdependencies are identified and documented. |
| MAP 1.3 | Stakeholder impact | Potential impacts on individuals, groups, communities, organizations, and society are identified. |
| MAP 1.5 | Benefits assessment | Expected benefits of the AI system are documented alongside risks. |
| MAP 1.6 | Limitations | Known limitations and failure modes are identified and documented. |
| MAP 2 | Risk identification | AI risks are identified at each stage of the lifecycle. |
| MAP 2.1 | Scientific validity | The scientific basis and data quality of the AI approach are assessed. |
| MAP 2.2 | Bias identification | Sources of bias are identified across the AI lifecycle (design, data, model, deployment). |
| MAP 2.3 | Pre-deployment testing | Comprehensive testing including stress tests, adversarial tests, and red-teaming. |
| MAP 3 | Positive impact | Processes for identifying and promoting positive AI impacts are in place. |
| MAP 3.1 | Benefits tracking | Realized benefits are tracked and compared against expected benefits. |
| MAP 4 | Categorization | AI risks are categorized and prioritized. |
| MAP 4.1 | Risk taxonomy | A consistent taxonomy for categorizing AI risks is used. |
| MAP 4.2 | Risk prioritization | Risks are prioritized based on likelihood, severity, and reversibility. |
| MAP 5 | Risk alignment | Identified risks are aligned with organizational risk tolerance. |
| MAP 5.1 | Tolerance comparison | AI risks are compared against established risk tolerance thresholds. |

---

### MEASURE — Assessment and analysis

Quantifying, analyzing, and monitoring AI risks.

| Category | Subcategory | Description |
|----------|-------------|-------------|
| MEASURE 1 | Metrics | Appropriate metrics are identified and applied to assess AI risk. |
| MEASURE 1.1 | Performance metrics | Metrics for accuracy, reliability, robustness, and other performance dimensions. |
| MEASURE 1.2 | Fairness metrics | Metrics for assessing equity, bias, and fairness across demographic groups. |
| MEASURE 1.3 | Explainability metrics | Metrics for interpretability and explainability of AI outputs. |
| MEASURE 2 | Evaluation | AI systems are evaluated regularly against identified metrics. |
| MEASURE 2.1 | Pre-deployment evaluation | Comprehensive evaluation before deployment including validation testing. |
| MEASURE 2.2 | Post-deployment monitoring | Ongoing monitoring of deployed AI systems against performance thresholds. |
| MEASURE 2.3 | Bias testing | Regular testing for emergent biases in production environments. |
| MEASURE 2.4 | Red-teaming | Structured adversarial testing to identify vulnerabilities and failure modes. |
| MEASURE 2.5 | Independent evaluation | Independent third-party evaluation where appropriate. |
| MEASURE 3 | Tracking | AI risk metrics are tracked over time. |
| MEASURE 3.1 | Trend analysis | Historical trends in AI risk metrics are analyzed to identify patterns. |
| MEASURE 3.2 | Drift detection | Data drift, concept drift, and model performance degradation are monitored. |
| MEASURE 4 | Feedback | Measurement results inform ongoing risk management. |
| MEASURE 4.1 | Feedback loops | Results from measurement activities feed back into governance and development processes. |

---

### MANAGE — Risk treatment and response

Actions to address identified risks based on measurement results.

| Category | Subcategory | Description |
|----------|-------------|-------------|
| MANAGE 1 | Risk treatment | Plans for addressing identified risks are developed and implemented. |
| MANAGE 1.1 | Mitigation strategies | Specific mitigation strategies for identified risks are documented and implemented. |
| MANAGE 1.2 | Risk acceptance | Residual risks are documented and formally accepted by appropriate authority. |
| MANAGE 1.3 | Prioritization | Risk treatment is prioritized based on severity, likelihood, and available resources. |
| MANAGE 2 | Risk response | Mechanisms for responding to AI incidents and failures are in place. |
| MANAGE 2.1 | Incident response | Procedures for responding to AI-related incidents including escalation and communication. |
| MANAGE 2.2 | Rollback | Ability to roll back or disable AI systems that are causing harm. |
| MANAGE 2.3 | Communication | Communication plans for informing affected parties about AI incidents. |
| MANAGE 2.4 | Recovery | Recovery procedures for restoring AI system operations after incidents. |
| MANAGE 3 | Continuous improvement | AI risk management processes are improved based on lessons learned. |
| MANAGE 3.1 | Post-incident review | Post-incident reviews are conducted and findings incorporated. |
| MANAGE 3.2 | Process improvement | Risk management processes are updated based on new threats, technologies, and lessons learned. |
| MANAGE 4 | Documentation | AI risk management activities are documented. |
| MANAGE 4.1 | Risk register | A risk register for AI systems is maintained and regularly updated. |
| MANAGE 4.2 | Audit trail | Decisions about AI development, deployment, and risk treatment are documented with rationale. |

---

## AI 600-1: Generative AI Risk Profile

Additional risk categories specific to generative AI systems:

### GenAI Risk Categories

| Risk Category | Description | Example Mitigations |
|--------------|-------------|-------------------|
| **CBRN Information** | GAI may provide information enabling chemical, biological, radiological, or nuclear threats | Content filtering, red-teaming, use-case restrictions |
| **Confabulation** | GAI generates false but plausible information ("hallucinations") | Grounding, retrieval-augmented generation, confidence scoring, human review |
| **Data Privacy** | GAI may memorize and reproduce training data including PII | Differential privacy, data deduplication, output filtering, PII detection |
| **Environmental** | Training and inference consume significant energy and water | Efficiency optimization, carbon tracking, model distillation |
| **Harmful Bias** | GAI may amplify biases present in training data | Bias testing across demographics, diverse training data, output monitoring |
| **Homogenization** | Over-reliance on a few foundation models reduces diversity of outputs | Model diversity, ensemble approaches, customization |
| **Information Integrity** | GAI can generate convincing disinformation at scale | Watermarking, provenance tracking, content authentication |
| **Information Security** | GAI introduces new attack vectors (prompt injection, data poisoning, model extraction) | Input validation, adversarial testing, access controls, model hardening |
| **Intellectual Property** | GAI may generate content infringing on copyrights or trademarks | Training data documentation, copyright filtering, attribution mechanisms |
| **Obscene/Degrading Content** | GAI may generate harmful, violent, or sexually explicit content | Content moderation, safety classifiers, RLHF alignment |
| **Dangerous Content** | GAI may provide instructions for harmful activities | Use-case restrictions, content filtering, red-teaming |
| **Human-AI Configuration** | Over-reliance on GAI or inappropriate levels of human oversight | Clear disclosure of AI use, human-in-the-loop for critical decisions |

### GenAI-Specific Actions (200+ suggested actions organized by GOVERN/MAP/MEASURE/MANAGE)

Key actions per function:

**GOVERN for GenAI:**
- Establish acceptable use policies specifically for generative AI
- Define roles responsible for reviewing and approving GAI outputs
- Implement training programs on GAI risks and limitations
- Establish policies on GAI-generated content disclosure

**MAP for GenAI:**
- Assess training data for representation and potential biases
- Document data provenance and consent for training data
- Identify downstream impacts of GAI adoption on workflows and employment
- Map intellectual property risks specific to GAI-generated content

**MEASURE for GenAI:**
- Evaluate confabulation rates across different domains and contexts
- Test for memorization and unintended data leakage
- Assess environmental impact of model training and inference
- Conduct red-teaming exercises targeting GAI-specific vulnerabilities

**MANAGE for GenAI:**
- Implement guardrails for GAI outputs (content filtering, safety classifiers)
- Establish human review workflows for high-stakes GAI applications
- Create incident response procedures for GAI-specific failures
- Monitor for emerging risks as GAI capabilities evolve

---

## Cross-Reference to ISO 42001

| NIST AI RMF Function | Related ISO 42001 Controls |
|----------------------|---------------------------|
| GOVERN | Clause 5 (Leadership), A.2 (Policies), A.3 (Organization) |
| MAP | Clause 6 (Planning), A.5.1-A.5.3 (Lifecycle planning, requirements, design) |
| MEASURE | Clause 9 (Performance evaluation), A.5.5 (Verification), A.8.4 (Monitoring) |
| MANAGE | Clause 10 (Improvement), A.8.5 (Incident management), Clause 8 (Operation) |

## Cross-Reference to EU AI Act

| NIST AI RMF Function | Related EU AI Act Articles |
|----------------------|---------------------------|
| GOVERN | Art. 9 (Risk management), Art. 17 (QMS) |
| MAP | Art. 9 (Risk identification), Art. 27 (Fundamental rights assessment) |
| MEASURE | Art. 15 (Accuracy/robustness), Art. 12 (Record-keeping) |
| MANAGE | Art. 14 (Human oversight), Art. 72 (Post-market monitoring), Art. 73 (Incident reporting) |
