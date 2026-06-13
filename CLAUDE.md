# BloggerAgents - AI-Powered French Blog Writing Crew

## Overview

BloggerAgents is a multi-agent AI system built with [crewAI](https://crewai.com) that automates the creation of French-language blog posts about expatriate life in Scotland (particularly Edinburgh). The project simulates a editorial team of specialized AI agents that collaborate to research, plan, write, optimize, edit, and quality-check articles.

## Architecture

### Agents (6 total)

| Agent | LLM | Purpose |
|-------|-----|---------|
| `researcher` | gpt-4o | Expatriation expert - finds official sources (gov.uk, NHS Écosse, etc.) and expat blogs |
| `planner` | gpt-4o | Content strategist - builds narrative article structure |
| `seo_optimizer` | gpt-4o-mini | SEO specialist for French expat niche |
| `writer` | gpt-4o | Expat blogger - writes warm, personal French content |
| `editor` | gpt-4o | Stylistic editor - applies personal style guide |
| `quality_reviewer` | gpt-4o-mini | Fact-checker & French language reviewer |

### Workflow (Sequential Process)

1. **Research** → 2. **Planning** → 3. **Writing** → 4. **SEO Optimization** → 5. **Editing** → 6. **Quality Review** → Article

### Configuration Files

- `src/blogger_agents/config/agents.yaml` - Agent definitions (roles, goals, backstories)
- `src/blogger_agents/config/tasks.yaml` - Task definitions with expected outputs
- `src/blogger_agents/crew.py` - Crew orchestration with tool integrations
- `src/blogger_agents/main.py` - Entry point with topic/keyword inputs
- `knowledge/style_guide.md` - Personal writing style guide (applied to editor)

## Project Setup

```bash
# Install dependencies
uv sync

# Set API key
echo "OPENAI_API_KEY=your_key" > .env

# Run the crew
crewai run

# Or directly
python -m blogger_agents.main
```

## Key Characteristics

- **Language**: All content is written in French for French-speaking readers
- **Niche**: Expatriation in Scotland - administrative, cultural, practical content
- **Style**: "Bienveillant et Pragmatique" - warm, pragmatic, personal tone
- **Author persona**: French expat living in Edinburgh with family
- **Comparisons**: Often references Lyon (France) for context

## Output

Articles are saved to `articles/final_version_YYYY-MM-DD_HH-MM.md` and include:
- SEO-optimized title and meta description
- Main article content in Markdown
- Sources and links section
- Journal of corrections made

## Custom Tools

- `src/blogger_agents/tools/custom_tool.py` - Template for adding custom tools
- `crewai_tools.SerperDevTool` - Web search tool used by researcher

## Testing

Tests directory exists but is empty. Add tests in `tests/`.

## Local Development

The project uses a `.env` file for secrets (gitignored). The `.venv` virtual environment is tracked in git (though `.venv/` is in `.gitignore`).
