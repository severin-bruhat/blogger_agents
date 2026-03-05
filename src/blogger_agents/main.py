#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from blogger_agents.crew import BloggerAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    inputs = {
        'topic': 'Comment obtenir la nationalité britannique en habitant en Écosse? Condiderer la procedure et les frais',
        'word_count': '1200',
        'keyword': 'passeport britannique écosse nationalité',
        'timestamp': now
    }

    try:
        BloggerAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

