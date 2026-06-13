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

    topic = (
        "Festival du Fringe à Edimbourg"
    )
    keyword = "Ecosse"
    word_count = 1500
    
    inputs = {
        'topic': topic,
        'word_count': word_count,
        'keyword': keyword,
        'timestamp': now
    }



    try:
        BloggerAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

