import os
from datetime import datetime

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

os.environ["SERPER_API_KEY"] = "your_serper_api_key"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

@CrewBase
class ReportingCrew:
    """Crew for Generating RCA Reports"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    llm = ChatOpenAI(model="gpt-4o-mini")

    @agent
    def technical_rca_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_rca_reporter"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )

    @agent
    def non_technical_rca_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["non_technical_rca_reporter"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )

    @agent
    def internet_researcher(self) -> Agent:
        serper_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["internet_researcher"],
            tools=[serper_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )

    @task
    def analyze_logs(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_logs"],
            agent=self.technical_rca_reporter()
        )

    @task
    def search_for_similar_failures(self) -> Task:
        return Task(
            config=self.tasks_config["search_for_similar_failures"],
            agent=self.internet_researcher()
        )

    @task
    def generate_technical_report(self) -> Task:
        return Task(
            config=self.tasks_config["generate_technical_report"],
            agent=self.technical_rca_reporter(),
            allow_code_execution=True,
            output_file=f"results/technical-rca_{self.current_time}.md",
            context=[self.analyze_logs(), self.search_for_similar_failures()]
        )

    @task
    def generate_non_technical_report(self) -> Task:
        
        return Task(
            config=self.tasks_config["generate_non_technical_report"],
            agent=self.non_technical_rca_reporter(),
            output_file=f"results/non-technical-rca_{self.current_time}.md",
            context=[self.analyze_logs(), self.search_for_similar_failures()]
        )

    @crew
    def crew(self) -> Crew:
        """RCA Reporting Crew"""
        return Crew(
            agents=[
                self.technical_rca_reporter(),
                self.non_technical_rca_reporter(),
                self.internet_researcher()
            ],
            tasks=[
                self.analyze_logs(),
                self.search_for_similar_failures(),
                self.generate_technical_report(),
                self.generate_non_technical_report()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True
        )        