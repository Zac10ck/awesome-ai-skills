"""Editorially reviewed discovery queue batch, 2026-10-23."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/resources.json'
rows=json.loads(path.read_text())
batch=[
 ('datamimic-ce','DATAMIMIC Community Edition','ai-tool','data-analytics','rapiddweller/datamimic','Deterministic synthetic-data and pseudonymization engine with CLI and optional MCP adapter; enterprise governance features are separate.',['Python','MCP clients'],['synthetic-data','finance','healthcare','testing']),
 ('datamimic-generate-skill','DATAMIMIC Generate Test Data','agent-skill','software-testing','rapiddweller/datamimic/tree/development/plugins/datamimic/skills/generate-test-data','Agent skill for authoring and verifying DATAMIMIC synthetic test-data projects using the Community Edition CLI.',['Codex','Claude Code'],['test-data','synthetic-data']),
 ('healthcare-evidence-mcp','Healthcare Evidence Agent','mcp-server','healthcare-ai','Akhilesh-Vangala/healthcare-evidence-agent','Research agent and MCP tools for FDA labels, clinical trials, and Medicare coverage evidence with citation checks; public data only.',['Claude Code'],['fda','clinical-trials','evidence']),
 ('healthcare-citation-skill','Cited Healthcare Evidence','agent-skill','healthcare-ai','Akhilesh-Vangala/healthcare-evidence-agent/tree/main/agent_workspace/.claude/skills/cited-evidence','Claude skill for healthcare evidence synthesis with retrieved-source citations and quote verification; not clinical decision support.',['Claude Code'],['citations','research']),
 ('evidence-deflator','Evidence Deflator','ai-tool','trading-research','Beltran12138/evidence-deflator','Trading research tools for examining backtest leakage, selection effects, and public wallet evidence; includes MCP integration.',['Python','MCP clients'],['backtesting','research','evaluation']),
 ('calendar-reminders-skill','Manage Calendar and Reminders','agent-skill','organization-work','Austrust/harness-productivity-cli/tree/main/skills/manage-calendar-reminders','Agent skill using Python CLIs for CalDAV or Microsoft Graph calendars and iCloud reminders; requires local authentication.',[],['calendar','reminders','organization']),
 ('allneurons-contract-dashboard','Contract Dashboards','agent-skill','organization-work','allNeurons-AI/back-office-agents/tree/main/legal/skills/agiloft-dashboards','Claude skill for read-only contract reporting and dashboards from connected systems, spreadsheets, and documents.',['Claude Code'],['contracts','reporting','operations']),
 ('allneurons-flux','GL Account Flux Explainer','agent-skill','finance-accounting','allNeurons-AI/back-office-agents/tree/main/finance/skills/allneurons-flux','Claude skill for explaining period-to-period general-ledger changes with source details and Excel output.',['Claude Code'],['accounting','variance-analysis']),
 ('allneurons-tb-rollforward','Trial Balance Roll-Forward','agent-skill','finance-accounting','allNeurons-AI/back-office-agents/tree/main/finance/skills/tb-rollforward','Claude skill for trial-balance roll-forwards, month-end baselines, and multi-entity reporting workbooks.',['Claude Code'],['accounting','close-management']),
 ('canary-risk-desk','Canary','ai-tool','trading-research','osauer/canary','Local Interactive Brokers research desk with portfolio briefs and read-only MCP tools; MCP cannot execute orders.',['MCP clients'],['portfolio','risk','interactive-brokers']),
 ('taiwan-health-mcp','Taiwan Health MCP','mcp-server','healthcare-ai','healthymind-tech/Taiwan-Health-MCP','Taiwan-focused medical terminology, drug-data, and FHIR validation tools; assess clinical suitability independently.',['MCP clients'],['taiwan','fhir','terminology']),
 ('orbit-crm','Orbit CRM MCP','mcp-server','organization-work','tobiaswuerth/orbit','Local Markdown-vault CRM for contacts, organizations, interactions, and follow-up tasks through MCP.',['MCP clients'],['crm','obsidian','organization']),
]
for id,name,type,category,repo,description,compatibility,tags in batch:
 url='https://github.com/'+repo
 if any(r['id']==id or r['url'].lower().rstrip('/')==url.lower().rstrip('/') for r in rows):continue
 rows.append(dict(id=id,name=name,type=type,category=category,url=url,description=description,source='community',compatibility=compatibility,tags=tags,verified_at='2026-10-23',maintenance='unknown',verification_note='Reviewed primary README, documented resource type, and canonical URL; no installation or professional validation performed.'))
path.write_text(json.dumps(rows,indent=2)+'\n')
print(f'{len(rows)} resources')
