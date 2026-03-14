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
        "Les 3 musées incontournables à visiter à Édimbourg : "
        "le National Museum of Scotland, la Scottish National Gallery et le Museum of Edinburgh — "
        "histoire, collections phares, infos pratiques (horaires, tarifs, accès) "
        "et conseils pour bien organiser sa visite en famille ou entre amis"
    )
    keyword = "musées à visiter Édimbourg"
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

