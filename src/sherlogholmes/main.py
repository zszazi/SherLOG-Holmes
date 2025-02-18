#!/usr/bin/env python
import datetime
import json
import os
from random import randint

from crewai.flow import Flow, and_, listen, or_, router, start
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace
from pydantic import BaseModel

from sherlogholmes.crews.alert_response_crew.alert_response_crew import (
    AlertResponseCrew,
)
from sherlogholmes.crews.customer_communication_crew.customer_communication_crew import (
    CustomerCommunicationCrew,
)
from sherlogholmes.crews.log_analysis_crew.log_analysis_crew import AnalysisCrew
from sherlogholmes.crews.rca_crew.rca_crew import ReportingCrew
from sherlogholmes.crews.war_room_crew.war_room_crew import WarRoomCrew
from src.sherlogholmes._types import SherLOGState

load_dotenv()

langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"),service_name ="sherLOGholmes")

class SherLOGFlow(Flow[SherLOGState]):

    @start()
    def assemble_crews(self):
        print("Assembling Crews")
        os.makedirs("results", exist_ok=True)
        self.state.started_at = datetime.datetime.now()

    @listen(assemble_crews)
    def log_analysis(self):
        resultjobs = (
            AnalysisCrew().crew().kickoff(inputs={"jobid_result_json": "logs/jobsStatus.json", 
                                                "py_logs" : "logs/py_job_logs.log", 
                                                "dns_logs" : "logs/dns_job_logs.log"}) #TODO: All the inputs are overwritten at agent level for testing revert this later
        )
        print("LOG ANALYSIS RESULTS", resultjobs.raw)
        self.state.log_analysis = resultjobs.raw
        

    @listen(log_analysis)
    def impact_analysis(self):
        impact = (
            AlertResponseCrew().crew().kickoff(inputs={"log_data": self.state.log_analysis})
        )
        print("IMPACT ANALYSIS RESULTS", impact.raw)
        self.state.impact = impact.raw
        self.state.severity_score = impact.pydantic.data.impact_score
        
    @router(impact_analysis)
    def severity_routing(self):
        if self.state.severity_score >= 80:
            return "sev:high"
        else:
            return "sev:low"
        
    @listen(log_analysis)
    def rca(self):
        rca = (
            ReportingCrew().crew().kickoff(inputs={"log_data": self.state.log_analysis})
        )
        print("RCA RESULTS", rca.raw)
        self.state.rca = rca.raw
    
    @listen("sev:low")
    def low_sev(self):
        print("dont panic")

    @listen(and_("sev:high", rca))
    def cust_comm(self):
        cust_comm = CustomerCommunicationCrew().crew().kickoff(inputs={"rca_analysis": self.state.rca})
        print("CUSTOMER RESULTS", cust_comm.raw)
        self.state.cust_comm = cust_comm.raw

    
    @listen("sev:high")
    def war_room(self):
        war_room = (
            WarRoomCrew().crew().kickoff(inputs={"log_data": self.state.log_analysis, "impact_analysis": self.state.impact})
        )
        print("WAR ROOM RESULTS", war_room.raw)
        self.state.war_room = war_room.raw


    @listen(or_(and_(cust_comm, war_room),low_sev))
    def teardown(self):
        file_path = "results/crew_results.json"

        try:
            if hasattr(self.state, "dict"):
                state_data = self.state.dict()
            else:
                state_data = self.state.__dict__

            with open(file_path, "w", encoding="utf-8") as f:
                state_data["started_at"] = state_data["started_at"].isoformat()
                json.dump(state_data, f, indent=2)
            
            print(f"state json save at {file_path}")

        except Exception as e:
            print(f"Error saving state json: {e}")

        
def kickoff():
    sherlog_flow = SherLOGFlow()
    sherlog_flow.kickoff()


def plot():
    sherlog_flow = SherLOGFlow()
    sherlog_flow.plot()


if __name__ == "__main__":
    plot()
    kickoff()





