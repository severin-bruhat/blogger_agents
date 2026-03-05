from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

smart_llm = LLM(model="gpt-4o")
fast_llm = LLM(model="gpt-4o-mini")

with open("knowledge/style_guide.md", "r", encoding="utf-8") as f:
    personal_style_guide = f.read()

@CrewBase
class BloggerAgents():
    """BloggerAgents crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    
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