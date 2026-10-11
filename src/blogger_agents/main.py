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
        "Rédigez un article pour de bons plans pour visiter Edimbourg à pied en mode nature. "
        "Inclure: Calton Hill, Arthur seat (et les autres colines), water of leith walk, the shore, the Botanic Garde,"
        "et autres endroits naturels en centre ville (ou proche)."
    )

    # Auto-extract keyword if not provided
    keyword = extract_keywords_from_prompt(prompt)
    word_count = 2000

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
