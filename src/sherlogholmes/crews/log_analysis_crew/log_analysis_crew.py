from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool
from crewai_tools import FileReadTool
from langchain_openai import ChatOpenAI

from src.sherlogholmes._types import AggregatorList, FailureJobs, LogsFailureList


@CrewBase
class AnalysisCrew:
    """Initial Log Analysis Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    llm = ChatOpenAI(model="gpt-4o-mini")

    def __init__(self, task_dir):
        self.results = {}
        self.task_dir = task_dir

    def store_output(self, task_name: str, output):
        self.results[task_name] = output

    @agent
    def job_extractor(self) -> Agent:
        file_read_tool = FileReadTool(f"{self.task_dir}/jobsStatus.json")
        return Agent(
            config=self.agents_config["job_extractor"],
            tools=[file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )

    @agent
    def py_log_parser(self) -> Agent:
        file_read_tool = FileReadTool(f"{self.task_dir}/py_job_logs.log")
        return Agent(
            config=self.agents_config["py_log_parser"],
            tools=[file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
        )
    
    @agent
    def dns_log_parser(self) -> Agent:
        file_read_tool = FileReadTool(f"{self.task_dir}/dns_job_logs.log")
        return Agent(
            config=self.agents_config["dns_log_parser"],
            tools=[file_read_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2
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
    def extract_failed_jobs(self) -> Task:
        return Task(
            config=self.tasks_config["extract_failed_jobs"],
            output_pydantic=FailureJobs,
            callback=lambda output: self.store_output("failed_jobs", output) 
        )

    @task
    def analyze_python_logs(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_python_logs"], 
            output_pydantic=LogsFailureList,
            context=[self.extract_failed_jobs()],
            callback=lambda output: self.store_output("application_logs", output) 
        )
    
    @task
    def analyze_dns_logs(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_dns_logs"], 
            agent= self.dns_log_parser(),
            output_pydantic=LogsFailureList,
            context=[self.extract_failed_jobs()],
            callback=lambda output: self.store_output("network_logs", output) 
        )
    
    def aggregate_results(self, ctx):
        aggregated_output = {
        "failed_jobs": ctx.get(self.extract_failed_jobs(), {}),
        "application_logs": ctx.get(self.analyze_python_logs(), {}),
        "network_logs": ctx.get(self.analyze_dns_logs(), {})
        }
    
        self.store_output("aggregator_task", aggregated_output)
        return aggregated_output

    @task
    def aggregate_results_task(self) -> Task:
        return Task(
        description="Aggregate all collected failure logs into a single report.",
        expected_output="A combined report of all failure logs.",
        context=[self.extract_failed_jobs(), self.analyze_python_logs(), self.analyze_dns_logs()],
        execution=lambda ctx: self.aggregate_results(ctx), 
        agent=self.aggregator(),
        output_file=f"{self.task_dir}/failure_logs.md"
        )
    
    @crew
    def crew(self) -> Crew:
        """Log Analysis Crew"""
        # return Crew(
        #     agents=self.agents,
        #     tasks=self.tasks,
        #     # process=Process.hierarchical,
        #     verbose=True,
        #     memory=True,
        #     # manager_llm="gpt-4o-mini"
        # )
        return Crew(
        agents=self.agents,  
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,
        memory=True
        )
        
