"""Reproducible editorial seed batch; URL checks are performed separately."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
categories = json.loads((ROOT / 'data/categories.json').read_text())
resources = [r for r in json.loads((ROOT / 'data/resources.json').read_text()) if r['id'] != 'microsoft-biomednlp']
groups = {
 'trading-research': ('Trading & Quantitative Research', 'Research, backtesting, and market-data tools. Backtests do not establish future returns.'),
 'finance-accounting': ('Finance & Accounting', 'Financial language models, accounting, reporting, and financial research resources.'),
 'healthcare-ai': ('Healthcare & Life Sciences', 'Medical AI research and biomedical tooling; inclusion does not establish clinical validation.'),
 'organization-work': ('Organization & Team Operations', 'Knowledge, project management, team collaboration, and organizational automation.'),
 'blogs-research': ('Blogs, Research & Discovery', 'Primary engineering blogs, research publications, and established curated directories.'),
}
rows = '''trading-research|AI4Finance-Foundation/FinRL|FinRL|framework|Reinforcement learning framework for quantitative finance and trading research.
trading-research|microsoft/qlib|Qlib|framework|Microsoft quantitative investment research platform for data, modeling, and strategy evaluation.
trading-research|freqtrade/freqtrade|Freqtrade|open-source-app|Crypto strategy research, backtesting, optimization, and trading automation platform.
trading-research|quantopian/zipline|Zipline|library|Event-driven algorithmic trading backtesting engine and research reference.
trading-research|kernc/backtesting.py|Backtesting.py|library|Python framework for simulating and analyzing trading strategies on historical data.
trading-research|polakowo/vectorbt|vectorbt|library|Vectorized Python tools for quantitative strategy exploration and portfolio backtesting.
trading-research|QuantConnect/Lean|LEAN|framework|Open-source algorithmic trading engine for research, backtesting, and execution integrations.
finance-accounting|AI4Finance-Foundation/FinGPT|FinGPT|framework|Open-source financial language-model research, datasets, and application examples.
finance-accounting|AI4Finance-Foundation/FinNLP|FinNLP|library|Financial natural-language processing data pipelines and research tooling.
finance-accounting|AI4Finance-Foundation/Awesome_AI4Finance|Awesome AI4Finance|awesome-list|Curated financial AI research, models, datasets, and quantitative tooling.
finance-accounting|beancount/beancount|Beancount|open-source-app|Plain-text double-entry accounting system for programmable financial workflows.
finance-accounting|frappe/books|Frappe Books|open-source-app|Open-source desktop bookkeeping application for small-business accounting.
healthcare-ai|Project-MONAI/MONAI|MONAI|framework|PyTorch-based toolkit for deep learning research in healthcare imaging.
healthcare-ai|google-health/medgemma|MedGemma|framework|Google Health resources and examples for medical multimodal model research.
healthcare-ai|scverse/scanpy|Scanpy|library|Scalable Python toolkit for analyzing single-cell gene expression data.
healthcare-ai|DeepChem/deepchem|DeepChem|framework|Machine-learning framework for molecular, chemical, and life-science research.
healthcare-ai|TorchIO-project/torchio|TorchIO|library|Tools for loading, preprocessing, augmenting, and sampling medical images.
healthcare-ai|microsoft/BiomedNLP|BiomedNLP|framework|Microsoft biomedical natural-language processing models and research resources.
organization-work|langgenius/dify|Dify|open-source-app|Platform for building AI workflows, knowledge applications, and agents.
organization-work|FlowiseAI/Flowise|Flowise|open-source-app|Visual tools for composing language-model workflows and agent applications.
organization-work|onyx-dot-app/onyx|Onyx|open-source-app|Enterprise AI search and assistant platform connected to organizational knowledge.
organization-work|outline/outline|Outline|open-source-app|Collaborative team knowledge base with search, documents, and integrations.
organization-work|makeplane/plane|Plane|open-source-app|Project management platform for issues, cycles, roadmaps, and team planning.
organization-work|twentyhq/twenty|Twenty|open-source-app|Open-source CRM for organizing customer records, relationships, and team workflows.
organization-work|docmost/docmost|Docmost|open-source-app|Collaborative documentation and wiki platform for organizational knowledge.
blogs-research|Shubhamsaboo/awesome-llm-apps|Awesome LLM Apps|awesome-list|Curated example applications for agents, retrieval, multimodal AI, and practical workflows.
blogs-research|e2b-dev/awesome-ai-agents|Awesome AI Agents|awesome-list|Community collection of AI agent projects and application examples.
blogs-research|dair-ai/Prompt-Engineering-Guide|Prompt Engineering Guide|guide|Community educational guide to prompting methods, research, and language-model applications.
blogs-research|f/awesome-chatgpt-prompts|Awesome ChatGPT Prompts|awesome-list|Community prompt examples for writing, productivity, coding, and general assistant tasks.'''
known = {r['url'].lower().rstrip('/') for r in resources}
for key, (name, description) in groups.items():
 if key not in {c['id'] for c in categories}:
  categories.append(dict(id=key, name=name, description=description))
for line in rows.splitlines():
 category, repo, name, kind, description = line.split('|')
 if repo == 'microsoft/BiomedNLP':
  continue
 url = 'https://github.com/' + repo
 if url.lower().rstrip('/') in known:
  continue
 resources.append(dict(id=repo.lower().replace('/', '-').replace('_', '-').replace('.', '-'), name=name, type=kind, category=category, description=description, url=url, source='community', compatibility=[], tags=[category], verified_at=None, maintenance='unknown'))
 known.add(url.lower().rstrip('/'))
for name, url, description in [
 ('Hugging Face Blog', 'https://huggingface.co/blog', 'Engineering articles, model releases, datasets, and open-source machine-learning tutorials.'),
 ('Google Research Blog', 'https://research.google/blog/', 'Primary research announcements and technical articles from Google Research.'),
 ('Microsoft Research Blog', 'https://www.microsoft.com/en-us/research/blog/', 'Research publications and technical perspectives from Microsoft Research.'),
 ('Anthropic Engineering', 'https://www.anthropic.com/engineering', 'Engineering articles on agents, context, evaluations, and practical AI systems.'),
 ('Lilian Weng Blog', 'https://lilianweng.github.io/', 'Detailed technical literature reviews on machine learning, language models, and agents.'),
]:
 if url not in {r['url'] for r in resources}:
  resources.append(dict(id=name.lower().replace(' ', '-'), name=name, type='guide', category='blogs-research', description=description, url=url, source='community', compatibility=[], tags=['research', 'blog'], verified_at=None, maintenance='unknown'))
for file, value in [('categories.json', categories), ('resources.json', resources)]:
 (ROOT / 'data' / file).write_text(json.dumps(value, indent=2) + '\n')
print(f'{len(resources)} resources; {len(categories)} categories')
