# Installing compliance-auditor

## Method 1: Claude Code Plugin (Recommended)

### From your marketplace
```bash
# Users add your marketplace first (one-time)
/plugin marketplace add AdhithyaR/compliance-auditor

# Then install the plugin
/plugin install compliance-auditor
```

### From local directory
```bash
# Clone the repo
git clone https://github.com/AdhithyaR/compliance-auditor.git

# Install as a user-scoped plugin (available in all projects)
claude plugin install ./compliance-auditor --user

# Or project-scoped (shared with team via git)
claude plugin install ./compliance-auditor --project
```

Once installed, the skill is available as:
- **Slash command**: `/compliance-auditor` — invoke explicitly
- **Auto-trigger**: Claude detects compliance-related queries and loads it automatically

## Method 2: Manual Skill Install (Claude Code or Cowork)

```bash
# Personal (available everywhere)
cp -r skills/compliance-auditor ~/.claude/skills/compliance-auditor

# Project-level (shared with team via git)
cp -r skills/compliance-auditor .claude/skills/compliance-auditor
```

Verify with:
```
/skills
```
You should see `compliance-auditor` in the list.

## Method 3: Claude.ai Web (Upload .skill file)

1. Download `compliance-auditor.skill` from Releases
2. In Claude.ai, go to **Settings** (gear icon)
3. Navigate to the **Skills** section  
4. Click **Upload Skill** and select the `.skill` file
5. The skill activates automatically when you mention compliance topics

## Method 4: npx Quick Install

```bash
# If published to the skills registry
npx skills add https://github.com/AdhithyaR/compliance-auditor
```

## Method 5: Cowork

```bash
# Cowork picks up skills from ~/.claude/skills/ automatically
cp -r skills/compliance-auditor ~/.claude/skills/

# Or use the plugin system
/plugin install compliance-auditor
```

## Verify Installation

After installing, test with any of these prompts:

```
/compliance-auditor

"Check if we're SOC 2 ready"

"Analyze these documents against ISO 27001"

"Score this vendor questionnaire"

"What's missing for our HIPAA audit?"
```

## Optional: Enterprise Connectors

For maximum power, install the CLI integrations:

```bash
# Google Workspace (Drive, Gmail, Calendar, Sheets)
npm install -g @googleworkspace/cli
gws auth setup && gws auth login -s drive,docs,sheets,gmail,calendar

# Microsoft 365 (OneDrive, SharePoint, Entra ID, Purview, Teams)
npm install -g @pnp/cli-microsoft365
m365 setup && m365 login
```

The skill auto-detects available connectors at runtime.
