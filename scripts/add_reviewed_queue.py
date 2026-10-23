"""Editorially reviewed discovery queue batch, 2026-10-23."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'data/resources.json'
rows=json.loads(path.read_text())
batch=[
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
