from datetime import datetime
from pathlib import Path
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

TODAY = datetime.utcnow().strftime('%Y-%m-%d')
DISPLAY_DATE = datetime.utcnow().strftime('%B %d, %Y')

PROMPT = '''Search for the latest AI news and discussions across The Rundown AI, Ben’s Bites, The Neuron, TLDR AI, Hacker News, Simon Willison, Latent Space, Anthropic Engineering, OpenAI News, Awwwards, Codrops, n8n, LangChain, Reddit AI coding communities, and related developer sources. Create a detailed daily intelligence briefing focused on AI coding, CLI workflows, coding agents, automation, web design trends, MCP, subagents, context engineering, and practical operator insights. Review Hacker News comments carefully to identify hidden gems and emerging patterns. Avoid repeating stories from prior days unless there is a significant update or new development. Include practical implications, strategic analysis, operator insights, and implementation recommendations, not just headlines.'''

response = client.responses.create(
    model='gpt-5',
    input=PROMPT
)

content = response.output_text

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Operator Intelligence - {DISPLAY_DATE}</title>
<link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
<div class="noise"></div>
<header class="brief-header">
<nav class="nav">
<a class="back-link" href="../index.html">← Dashboard Home</a>
</nav>
<section class="brief-hero">
<div class="eyebrow">Daily Brief · {DISPLAY_DATE}</div>
<h1>AI Operator Intelligence</h1>
<p>Daily intelligence for AI coding, automation, MCP, CLI agents, UX trends, and operator workflows.</p>
</section>
</header>
<main class="brief-main">
<article class="brief-content">
<section class="brief-section">
<span class="chip blue">Daily Intelligence</span>
<pre style="white-space:pre-wrap;font-family:inherit;color:#cbd5e1;background:none;border:none;">{content}</pre>
</section>
</article>
</main>
</body>
</html>'''

archive_dir = Path('archive')
archive_dir.mkdir(exist_ok=True)

brief_path = archive_dir / f'{TODAY}.html'
brief_path.write_text(html, encoding='utf-8')

index_path = Path('index.html')
index_html = index_path.read_text(encoding='utf-8')

index_html = index_html.replace('archive/2026-05-13.html', f'archive/{TODAY}.html')
index_html = index_html.replace('May 13, 2026', DISPLAY_DATE)

index_path.write_text(index_html, encoding='utf-8')

archive_json = Path('data/archive.json')
existing = []
if archive_json.exists():
    existing = json.loads(archive_json.read_text())

entry = {
    'date': TODAY,
    'display_date': DISPLAY_DATE,
    'path': f'archive/{TODAY}.html'
}

existing = [e for e in existing if e['date'] != TODAY]
existing.insert(0, entry)

archive_json.write_text(json.dumps(existing, indent=2), encoding='utf-8')

print(f'Generated {brief_path}')
