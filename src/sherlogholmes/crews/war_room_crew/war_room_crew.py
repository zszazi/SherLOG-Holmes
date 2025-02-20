import json
import os

from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from langchain_openai import ChatOpenAI

from src.sherlogholmes._types import (
    ArchitecturalReviewReport,
    BusinessImpactReport,
    WarRoomActionPlan,
)


@CrewBase
class WarRoomCrew:
    """War Room Crew for Incident Resolution"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    llm = ChatOpenAI(model="gpt-4o-mini") 

    wiki_source = TextFileKnowledgeSource(
    file_paths=["wiki/architecture.txt", "wiki/network.txt"]
)
    def __init__(self, task_dir):
        self.results = {}
        self.task_dir = task_dir

    def store_output(self, task_name: str, output):
        self.results[task_name] = output

    @agent
    def senior_backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_backend_engineer"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False, 
            max_iter=1
        )

    @agent
    def senior_network_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_network_engineer"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False, 
            max_iter=1
        )

    @agent
    def principal_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["principal_architect"],
            llm=self.llm,
            verbose=True,
            max_iter=1,
            knowledge_sources=[self.wiki_source] # If failed -Bug in CrewAI - https://github.com/crewAIInc/crewAI/issues/2150
        )

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["product_manager"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False, 
            max_iter=1
        )
    

    @agent
    def aggregator(self) -> Agent:
        return Agent(
            config=self.agents_config["aggregator"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    @task
    def backend_issue_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["backend_issue_analysis"],
            agent=self.senior_backend_engineer(),
            callback=lambda output: self.store_output("backend_issue_analysis", output),
            expected_output="A markdown file of backend engineer analysis",
            output_file=f"{self.task_dir}/backend_engineer.md"
        )

    @task
    def network_issue_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["network_issue_analysis"],
            agent=self.senior_network_engineer(),
            callback=lambda output: self.store_output("network_issue_analysis", output),
            expected_output="A markdown file of network engineer analysis",
            output_file=f"{self.task_dir}/network_engineer.md"
        )

    @task
    def architectural_review(self) -> Task:
        return Task(
            config=self.tasks_config["architectural_review"],
            agent=self.principal_architect(),
            output_pydantic=ArchitecturalReviewReport,
            context=[self.backend_issue_analysis(), self.network_issue_analysis()],
            callback=lambda output: self.store_output("architectural_review", output)
        )

    @task
    def business_impact_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["business_impact_analysis"],
            agent=self.product_manager(),
            output_pydantic=BusinessImpactReport,
            callback=lambda output: self.store_output("business_impact_analysis", output)
        )

    @task
    def war_room_action_plan(self) -> Task:
        return Task(
            config=self.tasks_config["war_room_action_plan"],
            agent=self.principal_architect(),
            output_pydantic=WarRoomActionPlan,
            context=[
                self.backend_issue_analysis(), 
                self.network_issue_analysis(), 
                self.architectural_review(), 
                self.business_impact_analysis()
            ],
            callback=lambda output: self.store_output("war_room_action_plan", output)
        )
    
    @task
    def aggregate_results_task(self) -> Task:
        return Task(
        description="Aggregate all collected results into a single report.",
        expected_output="A combined report of all failure logs in form of markdown",
        output_file=f"{self.task_dir}/war_room.md",
        context=[self.backend_issue_analysis(), self.network_issue_analysis(), self.architectural_review(),self.business_impact_analysis(), self.war_room_action_plan()],
        agent=self.aggregator()
        )

    @crew
    def crew(self) -> Crew:
        """War Room Crew"""
        return Crew(
            agents=[
                self.senior_backend_engineer(),
                self.senior_network_engineer(),
                self.principal_architect(),
                self.product_manager(), 
                self.aggregator()
            ],
            tasks=[
                self.backend_issue_analysis(),
                self.network_issue_analysis(),
                self.architectural_review(),
                self.business_impact_analysis(),
                self.war_room_action_plan(), 
                self.aggregate_results_task()
            ],
            verbose=True,
            memory=True
        )






