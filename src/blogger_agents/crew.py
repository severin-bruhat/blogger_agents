from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from typing import List

smart_llm = LLM(model="gpt-4o")
fast_llm = LLM(model="gpt-4o-mini")

@CrewBase
class BloggerAgents():
    """BloggerAgents crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # Load your past articles to teach the Researcher your voice
        self.style_knowledge = PDFKnowledgeSource(
            file_paths=["style1.pdf", "style2.pdf", "style3.pdf"]
    )
    
    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], llm=fast_llm, verbose=True)

    @agent
    def planner(self) -> Agent:
        return Agent(config=self.agents_config['planner'], llm=fast_llm, verbose=True)

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
            knowledge_sources=[self.style_knowledge],
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
    def quality_review_task(self) -> Task:
        return Task(config=self.tasks_config['quality_review_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )