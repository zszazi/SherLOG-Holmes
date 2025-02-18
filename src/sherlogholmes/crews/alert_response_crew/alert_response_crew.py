from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai_tools import FileReadTool
from langchain_openai import ChatOpenAI

from src.sherlogholmes._types import ImpactScore, PagerDuty


@CrewBase
class AlertResponseCrew:
    """Initial Alert Response Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = ChatOpenAI(model="gpt-4o-mini")

    @agent
    def impact_assessor(self) -> Agent:
        return Agent(
            config=self.agents_config["impact_assessor"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    @agent
    def pagerduty_alert_sender(self) -> Agent: 
        return Agent(
            config=self.agents_config["pagerduty_alert_sender"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    @task
    def analyze_impact_and_categorize_failure(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_impact_and_categorize_failure"],
            output_pydantic=ImpactScore
        )
    
    @task
    def send_pagerduty_alert(self) -> Task:
        return Task(
            config=self.tasks_config["send_pagerduty_alert"],
            output_pydantic=PagerDuty,
            context=[self.analyze_impact_and_categorize_failure()]
        ) 

    @crew
    def crew(self) -> Crew:
        """Alert Response Crew"""
        return Crew(
        agents=self.agents,  
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
        )                   