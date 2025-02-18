import logging
import random
import time
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    filename="job_logs.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Sample job data (you can expand this to 30+ entries)
jobs = [
    {"jobId": "A1B2C3", "jobStatus": "Success", "jobRuntime": 120, "jobStart": "2025-03-10T12:30:00Z",
     "networkDetails": {"ipAddress": "192.168.1.1", "port": 8080, "protocol": "HTTPS", "latency": "20ms", "bandwidth": "100Mbps"}},
    {"jobId": "D4E5F6", "jobStatus": "Failure", "jobRuntime": 300, "jobStart": "2025-04-12T09:15:00Z",
     "networkDetails": {"ipAddress": "192.168.1.2", "port": 443, "protocol": "TCP", "latency": "50ms", "bandwidth": "50Mbps"}},
    {"jobId": "G7H8I9", "jobStatus": "Success", "jobRuntime": 180, "jobStart": "2025-05-22T16:45:00Z",
     "networkDetails": {"ipAddress": "192.168.1.3", "port": 22, "protocol": "SSH", "latency": "10ms", "bandwidth": "200Mbps"}},
    {"jobId": "J1K2L3", "jobStatus": "Failure", "jobRuntime": 250, "jobStart": "2025-06-30T14:00:00Z",
     "networkDetails": {"ipAddress": "192.168.1.4", "port": 3306, "protocol": "MySQL", "latency": "30ms", "bandwidth": "300Mbps"}},
    {"jobId": "M4N5O6", "jobStatus": "Success", "jobRuntime": 400, "jobStart": "2025-07-14T10:10:00Z",
     "networkDetails": {"ipAddress": "192.168.1.5", "port": 53, "protocol": "DNS", "latency": "5ms", "bandwidth": "500Mbps"}}
]

# Generate 300 log lines
for _ in range(300):
    job = random.choice(jobs)  # Pick a random job
    job_id = job["jobId"]
    status = random.choice(["Success", "Failure"])  # Randomly change success/failure
    runtime = random.randint(100, 500)  # Random job runtime
    network = job["networkDetails"]

    # Simulate a job execution timestamp
    log_time = datetime.utcnow() - timedelta(minutes=random.randint(1, 1000))

    # Log message format
    if status == "Success":
        logging.info(f"Job {job_id} completed successfully in {runtime} seconds. Network: {network}")
    else:
        logging.error(f"Job {job_id} failed after {runtime} seconds. Network: {network}")

    # Add some debug logs for network details
    logging.debug(f"Job {job_id}: Checking network status - IP: {network['ipAddress']}, Latency: {network['latency']}")

    # Simulate slight delay in log entries
    time.sleep(0.01)

print("Logs have been generated and saved to 'job_logs.log'.")
