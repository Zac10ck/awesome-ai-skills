"""Add the reviewed specialist expansion; verify URLs before publication."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / 'data/resources.json'
resources = json.loads(path.read_text())
rows = [
('alpaca-mcp','Alpaca MCP Server','trading-research','mcp-server','alpacahq/alpaca-mcp-server','Official Alpaca integration for market data, account inspection, and trading operations; use paper accounts for evaluation.'),
('financial-datasets-mcp','Financial Datasets MCP','finance-accounting','mcp-server','financial-datasets/mcp-server','Financial Datasets integration for company statements, stock prices, crypto data, and financial news.'),
('xero-mcp','Xero MCP Server','finance-accounting','mcp-server','XeroAPI/xero-mcp-server','Xero-maintained MCP integration for working with accounting data through authorized Xero accounts.'),
('tipranks-mcp','TipRanks MCP','finance-accounting','mcp-server','TipRanks/mcp','Official TipRanks MCP integration exposing financial market data and analyst research to compatible agents.'),
('bigdata-finance-plugins','Bigdata Financial Research Plugins','finance-accounting','skill-collection','Bigdata-com/bigdata-plugins-marketplace','Financial research skills and MCP setup resources using licensed financial data with citations.'),
('fhir-mcp','WSO2 FHIR MCP Server','healthcare-ai','mcp-server','wso2/fhir-mcp-server','Expose FHIR server capabilities through MCP for healthcare interoperability workflows; assess data access before use.'),
('atlassian-mcp','Atlassian MCP Server','organization-work','mcp-server','atlassian/atlassian-mcp-server','Official remote integration connecting authorized Atlassian projects, issues, and organizational knowledge to AI tools.'),
('knowledge-work-plugins','Anthropic Knowledge Work Plugins','organization-work','skill-collection','anthropics/knowledge-work-plugins','Official plugins with skills for finance, productivity, sales, marketing, data, and other knowledge-work tasks.'),
('pyhealth','PyHealth','healthcare-ai','framework','sunlabuiuc/PyHealth','Machine-learning toolkit for healthcare research using clinical datasets, predictive models, and evaluation pipelines.'),
('scispacy','scispaCy','healthcare-ai','library','allenai/scispacy','Allen Institute toolkit for biomedical text processing, named entities, and scientific-language pipelines.'),
('nnunet','nnU-Net','healthcare-ai','framework','MIC-DKFZ/nnUNet','Self-configuring deep-learning framework for biomedical image segmentation research and reproducible benchmarking.'),
('openproject','OpenProject','organization-work','open-source-app','opf/openproject','Project management platform for planning, tasks, timelines, collaboration, and organizational work tracking.'),
]
known={r['url'].lower().rstrip('/') for r in resources}
for id,name,category,type,repo,description in rows:
 url='https://github.com/'+repo
 if url.lower().rstrip('/') in known: continue
 resources.append(dict(id=id,name=name,category=category,type=type,url=url,description=description,source='official' if id not in ['pyhealth','nnunet'] else 'community',compatibility=['MCP clients'] if type=='mcp-server' else [],tags=[category],verified_at=None,maintenance='unknown'))
path.write_text(json.dumps(resources,indent=2)+'\n')
print(f'{len(resources)} resources')
