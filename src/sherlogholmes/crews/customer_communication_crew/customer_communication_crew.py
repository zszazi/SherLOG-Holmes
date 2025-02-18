import json
import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from src.sherlogholmes._types import CustomerEmail, FAQDocument


@CrewBase
class CustomerCommunicationCrew:
    """Crew for Customer-Facing Communication"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    llm = ChatOpenAI(model="gpt-4o-mini") 

    def __init__(self):
        self.results = {}

    def store_output(self, task_name: str, output):
        self.results[task_name] = output

    @agent
    def customer_support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_support_agent"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    @agent
    def human_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["human_reviewer"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,

        )
    
    @task
    def draft_customer_email(self) -> Task:
        return Task(
            config=self.tasks_config["draft_customer_email"],
            agent=self.customer_support_agent(),
            callback=lambda output: self.store_output("customer_email", output),
            output_file="results/customer_email.md"
        )

    @task
    def customer_faq_document(self) -> Task:
        return Task(
            config=self.tasks_config["customer_faq_document"],
            agent=self.customer_support_agent(),
            callback=lambda output: self.store_output("customer_faq_document", output),
            output_file="results/customer_faq.md"
        )
    
    @task
    def human_reviewer_task(self) -> Task:
        return Task(
            config=self.tasks_config["human_reviewer_task"],
            agent=self.human_reviewer(),
            callback=lambda output: self.store_output("human_reviewer", output),
            human_input=True
        )

    @crew
    def crew(self) -> Crew:
        """Customer Communication Crew"""
        return Crew(
            agents=[self.customer_support_agent(), self.human_reviewer()],
            tasks=[self.draft_customer_email(), self.customer_faq_document(), self.human_reviewer_task()],
            process=Process.sequential, 
            verbose=True,
            memory=True
        )

