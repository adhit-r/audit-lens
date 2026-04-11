# Enterprise Connector Reference

This file documents how to connect to enterprise document sources for evidence ingestion. The auditlens skill supports multiple storage backends — always detect which tools are available before attempting ingestion.

## Table of Contents
1. [Google Workspace via `gws` CLI](#gws)
2. [Microsoft 365 via `m365` CLI](#m365)
3. [Claude MCP Connectors](#mcp)
4. [Local Filesystem / Uploads](#local)
5. [Connector Detection Logic](#detection)

---

## 1. Google Workspace via `gws` CLI {#gws}

**Source**: https://github.com/googleworkspace/cli  
**Install**: `npm install -g @googleworkspace/cli`  
**Auth**: `gws auth setup` then `gws auth login -s drive,docs,sheets`

The `gws` CLI outputs structured JSON by default — perfect for programmatic evidence ingestion.

### Evidence Ingestion Commands

```bash
# List all files in a specific Drive folder (compliance evidence folder)
gws drive files list --params '{
  "q": "\"FOLDER_ID\" in parents",
  "pageSize": 100,
  "fields": "files(id,name,mimeType,modifiedTime,owners,description)"
}'

# Auto-paginate to get everything
gws drive files list --params '{
  "q": "\"FOLDER_ID\" in parents",
  "fields": "files(id,name,mimeType,modifiedTime,owners,description)"
}' --page-all

# Search for policy documents across entire Drive
gws drive files list --params '{
  "q": "fullText contains \"policy\" and mimeType != \"application/vnd.google-apps.folder\"",
  "pageSize": 50,
  "fields": "files(id,name,mimeType,modifiedTime,createdTime,owners)"
}'

# Download a specific file for analysis
gws drive files get --params '{"fileId": "FILE_ID", "alt": "media"}' > /tmp/evidence_doc.pdf

# Export Google Docs as PDF (native Docs can't be downloaded directly)
gws drive files export --params '{
  "fileId": "FILE_ID",
  "mimeType": "application/pdf"
}' > /tmp/policy.pdf

# Export Google Sheets as CSV
gws drive files export --params '{
  "fileId": "SHEET_ID",
  "mimeType": "text/csv"
}' > /tmp/asset_inventory.csv

# Get file metadata (for evidence dating and ownership)
gws drive files get --params '{
  "fileId": "FILE_ID",
  "fields": "id,name,mimeType,modifiedTime,createdTime,owners,lastModifyingUser,version,permissions"
}'

# Read Google Sheets directly (for asset inventories, risk registers)
gws sheets spreadsheets values get --params '{
  "spreadsheetId": "SPREADSHEET_ID",
  "range": "Sheet1!A1:Z500"
}'
```

### Useful Queries for Compliance Evidence

```bash
# Find all recently modified policies (last 90 days)
gws drive files list --params '{
  "q": "modifiedTime > \"2025-12-19T00:00:00\" and (name contains \"policy\" or name contains \"procedure\" or name contains \"standard\")",
  "orderBy": "modifiedTime desc"
}'

# Find stale documents (not modified in 18 months)
gws drive files list --params '{
  "q": "modifiedTime < \"2024-09-19T00:00:00\" and \"COMPLIANCE_FOLDER_ID\" in parents",
  "orderBy": "modifiedTime asc"
}'

# Find shared/external documents (potential data classification issues)
gws drive files list --params '{
  "q": "visibility = \"anyoneWithLink\" or visibility = \"anyoneCanFind\"",
  "fields": "files(id,name,permissions,shared)"
}'

# List all Google Forms (potential assessment/survey evidence)
gws drive files list --params '{
  "q": "mimeType = \"application/vnd.google-apps.form\"",
  "fields": "files(id,name,modifiedTime)"
}'
```

### Gmail — Policy Acknowledgment Evidence

```bash
# Search for policy acknowledgment emails
gws gmail users messages list --params '{
  "userId": "me",
  "q": "subject:(policy acknowledgment OR security awareness OR training completion)"
}'

# Triage inbox for compliance-relevant communications
gws gmail +triage
```

### Calendar — Review Cadence Evidence

```bash
# Check for recurring security review meetings
gws calendar +agenda --today

# Search for management review events
gws calendar events list --params '{
  "calendarId": "primary",
  "q": "management review OR security review OR risk review",
  "timeMin": "2025-01-01T00:00:00Z"
}'
```

---

## 2. Microsoft 365 via `m365` CLI {#m365}

**Source**: https://github.com/pnp/cli-microsoft365  
**Install**: `npm install -g @pnp/cli-microsoft365`  
**Auth**: `m365 setup` then `m365 login`  
**MCP Server**: `npm install -g @pnp/cli-microsoft365-mcp-server`

The `m365` CLI covers OneDrive, SharePoint, Teams, Outlook, Planner, Purview, and Entra ID.

### OneDrive Evidence Ingestion

```bash
# List files in a OneDrive folder
m365 onedrive list --webUrl "https://contoso-my.sharepoint.com/personal/user_contoso_com" \
  --folder "Compliance Evidence" --output json

# Download a file from OneDrive
m365 file get --webUrl "https://contoso-my.sharepoint.com/personal/user_contoso_com" \
  --url "/personal/user_contoso_com/Documents/Compliance/InfoSec-Policy.pdf" \
  --asFile --path /tmp/infosec-policy.pdf
```

### SharePoint Evidence Ingestion

SharePoint is where most enterprise compliance evidence lives — document libraries, wikis, lists.

```bash
# List all document libraries on a compliance site
m365 spo list list --webUrl "https://contoso.sharepoint.com/sites/compliance" \
  --filter "BaseTemplate eq 101" --output json

# List files in a SharePoint document library
m365 spo file list --webUrl "https://contoso.sharepoint.com/sites/compliance" \
  --folder "Shared Documents/Policies" --output json

# Download a file from SharePoint
m365 spo file get --webUrl "https://contoso.sharepoint.com/sites/compliance" \
  --url "/sites/compliance/Shared Documents/Policies/InfoSec-Policy.docx" \
  --asFile --path /tmp/infosec-policy.docx

# Search across all SharePoint sites for compliance docs
m365 spo search --queryText "policy OR procedure OR standard" \
  --selectProperties "Title,Path,LastModifiedTime,Author" --output json

# List SharePoint site permissions (access control evidence)
m365 spo site get --url "https://contoso.sharepoint.com/sites/compliance" --output json
```

### Microsoft Purview — Classification & Sensitivity Evidence

```bash
# List sensitivity labels (data classification evidence)
m365 purview sensitivitylabel list --output json

# Check retention labels
m365 purview retentionlabel list --output json
```

### Entra ID — Identity & Access Management Evidence

```bash
# List users (for access review evidence)
m365 entra user list --properties "displayName,userPrincipalName,accountEnabled,createdDateTime,lastSignInDateTime" --output json

# List groups (for RBAC evidence)
m365 entra group list --output json

# List app registrations (for OAuth/service account inventory)
m365 entra app list --output json

# Check conditional access policies (access control evidence)
m365 entra pim role assignment list --output json
```

### Teams — Communication & Collaboration Evidence

```bash
# List teams (for collaboration governance evidence)
m365 teams team list --output json

# List channels in a team
m365 teams channel list --teamId "TEAM_ID" --output json
```

### Planner — Task Management / Remediation Tracking

```bash
# List plans (potential remediation tracking)
m365 planner plan list --ownerGroupId "GROUP_ID" --output json

# List tasks in a plan
m365 planner task list --planId "PLAN_ID" --output json
```

---

## 3. Claude MCP Connectors {#mcp}

When running in Claude.ai or Claude Desktop, these native MCP connectors can supplement CLI-based access:

### Google Drive MCP (already connected in Claude.ai)
Use `google_drive_search` and `google_drive_fetch` tools directly — no CLI needed.

```
# Search for compliance documents
google_drive_search: fullText contains 'security policy'

# Fetch a specific Google Doc by ID
google_drive_fetch: document_id
```

### Gmail MCP (already connected in Claude.ai)
Search for policy acknowledgments, training completions, vendor communications.

### Google Calendar MCP (already connected in Claude.ai)
Verify management review cadence, security committee meetings.

### Linear MCP (if connected)
Track remediation tasks, map to compliance gaps.

### PostHog MCP (if connected)
Pull product analytics for processing integrity evidence.

---

## 4. Local Filesystem / Uploads {#local}

For files uploaded directly to the conversation or available on disk:

```bash
# Walk a local directory
find /mnt/user-data/uploads/ -type f \( -name "*.pdf" -o -name "*.docx" -o -name "*.xlsx" -o -name "*.csv" \)

# Or a specific compliance folder
find /path/to/compliance-evidence/ -type f -name "*.pdf" -exec stat -c '%n|%s|%y' {} \;
```

---

## 5. Connector Detection Logic {#detection}

At the start of every compliance audit session, detect which connectors are available:

```bash
# Check for gws CLI
command -v gws >/dev/null 2>&1 && echo "GWS_AVAILABLE=true" || echo "GWS_AVAILABLE=false"

# Check if gws is authenticated
gws drive files list --params '{"pageSize": 1}' 2>/dev/null && echo "GWS_AUTHENTICATED=true" || echo "GWS_AUTHENTICATED=false"

# Check for m365 CLI
command -v m365 >/dev/null 2>&1 && echo "M365_AVAILABLE=true" || echo "M365_AVAILABLE=false"

# Check if m365 is authenticated
m365 status --output json 2>/dev/null && echo "M365_AUTHENTICATED=true" || echo "M365_AUTHENTICATED=false"
```

If CLIs aren't available, fall back to:
1. Claude MCP connectors (Google Drive, Gmail, Calendar)
2. Direct file uploads from the user
3. Ask the user to install the relevant CLI

### Installation Helper

If the user needs to set up connectors, walk them through it:

```bash
# Google Workspace
npm install -g @googleworkspace/cli
gws auth setup
gws auth login -s drive,docs,sheets,gmail,calendar

# Microsoft 365
npm install -g @pnp/cli-microsoft365
m365 setup
m365 login
```
