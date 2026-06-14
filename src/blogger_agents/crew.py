from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
import re

smart_llm = LLM(model="gpt-4o")
fast_llm = LLM(model="gpt-4o-mini")

# Load the personal writing style guide to inject into relevant agents
with open("knowledge/style_guide.md", "r", encoding="utf-8") as f:
    personal_style_guide = f.read()


def extract_keywords_from_prompt(prompt: str) -> str:
    """
    Extract a keyword from a full sentence prompt for SEO optimization.
    Uses simple heuristics: finds the most relevant noun phrase or multi-word term.

    Args:
        prompt: Full sentence prompt (e.g., "Rédigez un article sur comment trouver
                un logement à Édimbourg quand on arrive...")

    Returns:
        A keyword string suitable for SEO (e.g., "logement Édimbourg")
    """
    # Remove common French starting phrases
    patterns_to_remove = [
        r'^Rédigez un article sur\s+',
        r'^Écrivez un article sur\s+',
        r'^Article sur\s+',
        r'^Écrivez sur\s+',
        r'^Rédigez sur\s+',
        r'^Écrivez une informations sur\s+',
        r'^Article à propos de\s+',
    ]

    cleaned = prompt
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)

    # Remove parentheses and their contents (optional details)
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)

    # Extract key phrases - look for prepositional phrases with important nouns
    # Key words for French expat blog SEO
    key_nouns = [
        r'\blogement\b', r'\bappartement\b', r'\bvisa\b', r'\bnationalité\b',
        r'\btravail\b', r'\bsalaire\b', r'\bcost of living\b', r'\bcout de la vie\b',
        r'\bÉdimbourg\b', r'\bEdimbourg\b', r'\bÉcosse\b', r'\bScotland\b',
        r'\bNHS\b', r'\bsettled status\b', r'\bpermis\b', r'\bconduire\b',
        r'\bfiscalité\b', r'\btax\b', r'\bcompte bancaire\b', r'\bbank account\b',
        r'\bécole\b', r'\bélèves\b', r'\bfamille\b', r'\bexpatrié\b', r'\bexpatriation\b'
    ]

    # Find matching key phrases
    found_keywords = []
    for noun_pattern in key_nouns:
        matches = re.findall(noun_pattern, cleaned, flags=re.IGNORECASE)
        if matches:
            found_keywords.extend(matches)

    if found_keywords:
        # Return the first found keyword, cleaned up
        return ' '.join(found_keywords[:3]).strip()

    # Fallback: extract first 2-3 significant words
    words = re.findall(r'\b[A-Z][a-zA-Zàéèùîïüâêôöë]\w*\b', cleaned)
    if words:
        return ' '.join(words[:3])

    # Ultimate fallback: first 3 non-stop words
    stop_words = {'à', 'au', 'aux', 'de', 'des', 'du', 'en', 'et', 'le', 'la',
                  'les', 'un', 'une', 'ou', 'où', 'ce', 'ces', 'pour', 'avec'}
    words = [w for w in cleaned.split() if w.lower() not in stop_words]
    return ' '.join(words[:3])[:50]  # Limit to 50 chars


@CrewBase
class BloggerAgents():
    """BloggerAgents crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    
    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], llm=smart_llm, tools=[SerperDevTool()], verbose=True)

    @agent
    def planner(self) -> Agent:
        return Agent(config=self.agents_config['planner'], llm=smart_llm, verbose=True)

    @agent
    def seo_optimizer(self) -> Agent:
        return Agent(config=self.agents_config['seo_optimizer'], llm=fast_llm, verbose=True)

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config['writer'], llm=smart_llm, verbose=True)

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'], 
            llm=smart_llm, 
            backstory=f"{self.agents_config['editor']['backstory']}\n\nSTYLE GUIDE TO FOLLOW:\n{personal_style_guide}",
            verbose=True
        )

    @agent
    def quality_reviewer(self) -> Agent:
        return Agent(config=self.agents_config['quality_reviewer'], llm=fast_llm, verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def planning_task(self) -> Task:
        return Task(config=self.tasks_config['planning_task'])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config['writing_task'])

    @task
    def seo_optimization_task(self) -> Task:
        return Task(config=self.tasks_config['seo_optimization_task'])

    @task
    def editing_task(self) -> Task:
        return Task(config=self.tasks_config['editing_task'])

    @task
    def verification_task(self) -> Task:
        return Task(
            description='''
                Effectuez une vérification croisée rapide des découvertes du chercheur
                avant de poursuivre avec la planification.

                Vérifications à effectuer:
                1. Confirmez que tous les faits de confiance élevée ont au moins 2 sources
                2. Identifiez les faits marqués comme faibles ou contradictoires
                3. Vérifiez la cohérence interne: pas de contradictions entre différentes parties
                4. Assurez-vous que les 5-8 questions fréquentes sont bien documentées

                Sortie: Un bref rapport de validation signalant:
                - Faits validés ✅
                - Faits nécessitant attention ⚠️
                - Recommandation: poursuivre avec planification OU demander recherche complémentaire
            ''',
            expected_output='''
                Rapport de vérification EN FRANÇAIS contenant:
                1. Statistiques: nombre total de faits, répartition par niveau de confiance
                2. Liste des points nécessitant clarification (avec suggestions de sources)
                3. Recommandation claire: [PROCEED TO PLANNING] ou [RETURN TO RESEARCHER WITH SPECIFIC NOTES]
                4. Tous les éléments en français
            ''',
            agent=self.quality_reviewer(),
            context=[self.research_task()]
        )

    @task
    def quality_review_task(self) -> Task:
        return Task(config=self.tasks_config['quality_review_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=[
                self.research_task(),
                self.verification_task(),
                self.planning_task(),
                self.writing_task(),
                self.seo_optimization_task(),
                self.editing_task(),
                self.quality_review_task()
            ],
            process=Process.sequential,
            verbose=True
        )