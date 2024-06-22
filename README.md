# Network Connections Analyzer

## Overview
This application analyzes network connections established by various programs running on your system. It uses `netstat` to fetch connection details and provides insights into external IP addresses, their reputation, and associated programs.

## Features
- Fetches network connections using `netstat`.
- Identifies external IP addresses and associated programs.
- Utilizes AbuseIPDB API for IP reputation scoring (requires API key).
- Falls back to IPApi.com in absence of AbuseIPDB key.
- Allows configuration of API keys through a settings window.

## Usage
1. **Installation**: Ensure Python and Tkinter are installed.


2. **Setup**:
- Run `pip install -r requirements.txt` to install dependencies.
- Ensure you have administrative privileges to fetch the processes.
3. **Run**:
   ```bash
   python main.py
   ```
    *(Optional)* To manually run with administrative privileges, right-click on the ``main.py`` file and select the ``Run as administrator`` option when running it.
  
   *The tool's initial appearance*.
  ![image](https://github.com/dannythedev/network_traffic_analyzer/assets/99733108/fce98fbe-7053-4799-b830-87b7ed8fd044)

- Click on the 'Get Processes' button to fetch and display network connections.
- *(Optional, but recommended for enhanced functionality)* Click on the settings button to input and save your API key.
- After viewing the processes, you'll see lists of programs and external IPs (outgoing traffic) below.
- Manually select IPs using your mouse or batch select by holding down the shift key from the external IP list.
- Confirm the selection to send specific external IPs to the third-party API.
- Click on the 'Send IPs' button and wait for the API to fetch and display the updated results on the initial process box.


