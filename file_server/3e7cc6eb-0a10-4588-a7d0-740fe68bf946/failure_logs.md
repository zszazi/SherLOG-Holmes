# Failure Logs Report

**Generated on:** 2025-04-12 12:00:00

## Aggregated Logs

### JobID: D4E5F6  
**IP:** 192.168.1.2  
**Application Logs (Python logs):**  
```
2025-02-10 16:30:34 - ERROR - Job D4E5F6 failed after 258 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:34 - ERROR - Job D4E5F6 failed after 316 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:34 - ERROR - Job D4E5F6 failed after 252 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:35 - ERROR - Job D4E5F6 failed after 207 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:35 - ERROR - Job D4E5F6 failed after 388 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:35 - ERROR - Job D4E5F6 failed after 450 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:35 - ERROR - Job D4E5F6 failed after 226 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:36 - ERROR - Job D4E5F6 failed after 411 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:36 - ERROR - Job D4E5F6 failed after 323 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:37 - ERROR - Job D4E5F6 failed after 168 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
2025-02-10 16:30:37 - ERROR - Job D4E5F6 failed after 126 seconds. Network: {'ipAddress': '192.168.1.2', 'port': 443, 'protocol': 'TCP', 'latency': '50ms', 'bandwidth': '50Mbps'}
```
**Network Logs (DNS logs):**  
```
[2025-04-12 09:15:10] WARNING - Connection attempt to 192.168.1.2 on port 443 using TCP.
[2025-04-12 09:15:15] ERROR   - High latency detected (50ms). Possible network congestion.
[2025-04-12 09:16:30] ERROR   - Connection timeout to 192.168.1.2. No response received.
[2025-04-12 09:17:00] ERROR   - Network failure. Retrying...
[2025-04-12 09:20:30] CRITICAL - Connection permanently lost to 192.168.1.2.
```

---

### JobID: J1K2L3  
**IP:** 192.168.1.4  
**Application Logs (Python logs):**  
```
2025-02-10 16:30:34 - ERROR - Job J1K2L3 failed after 367 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:35 - ERROR - Job J1K2L3 failed after 292 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:35 - ERROR - Job J1K2L3 failed after 208 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:35 - ERROR - Job J1K2L3 failed after 376 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:36 - ERROR - Job J1K2L3 failed after 350 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:36 - ERROR - Job J1K2L3 failed after 114 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:36 - ERROR - Job J1K2L3 failed after 444 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:36 - ERROR - Job J1K2L3 failed after 221 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:37 - ERROR - Job J1K2L3 failed after 386 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
2025-02-10 16:30:37 - ERROR - Job J1K2L3 failed after 369 seconds. Network: {'ipAddress': '192.168.1.4', 'port': 3306, 'protocol': 'MySQL', 'latency': '30ms', 'bandwidth': '300Mbps'}
```
**Network Logs (DNS logs):**  
```
[2025-06-30 14:00:10] WARNING - Attempting to connect to 192.168.1.4 on port 3306 using MySQL.
[2025-06-30 14:00:20] ERROR   - Slow response detected. Latency: 30ms.
[2025-06-30 14:01:45] ERROR   - Database connection failed. Possible firewall restriction.
[2025-06-30 14:03:00] CRITICAL - Connection to 192.168.1.4 terminated unexpectedly.
```

--- 

This report contains all collected failure logs for the specified jobs, categorized by job ID, application logs, and network logs, providing a comprehensive overview of the issues encountered.