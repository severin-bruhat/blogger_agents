#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from blogger_agents.crew import BloggerAgents, extract_keywords_from_prompt

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Full sentence prompt for detailed article instructions
    prompt = (
        "Rédigez un article sur comment trouver un logement à Édimbourg quand on arrive. "
        "Incluez: les sites web à utiliser (Target, Letgo, Flatmates), "
        "les zones recommandées (Leith, Newhaven, etc.), les zones à éviter (certains quartiers), "
        "le budget attendu (500-800£ par mois), et les pièges à éviter."
    )

    # Auto-extract keyword if not provided
    keyword = extract_keywords_from_prompt(prompt)
    word_count = 1500

    inputs = {
        'prompt': prompt,
        'word_count': word_count,
        'keyword': keyword,
        'timestamp': now
    }

    try:
        BloggerAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
