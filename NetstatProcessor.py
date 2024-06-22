import ipaddress
import math
import re
from tkinter import messagebox
from Functions import validate_and_expand_ip, extract_ip
from IPReputationClient import IpApiCom, AbuseIPDB
import subprocess


class NetstatProcessor:
    def __init__(self):
        self.external_ips = []
        self.program_names = dict()

    def fetch_netstat_data(self):
        result = subprocess.run(['netstat', '-anob'], capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return []

        netstat_output = result.stdout
        lines = netstat_output.splitlines()[4:]
        connections = []

        pattern = re.compile(r'^\s*(TCP|UDP)\s+([^\s]+)\s+([^\s]+)\s+([^\s]*)\s*([\d]+)?\s*(\[[^\]]+\])?')
        current_program = ''

        NO_PERMISSION_STRING = ('Can not obtain ownership information', 'N/A')
        EMPTY_STRING = ('', '-')

        for line in lines:
            match = pattern.match(line)
            if match:
                parts = list(filter(None, re.split(pattern, line.strip())))
                if len(parts) == 5:
                    protocol, local_addr, foreign_addr, state, pid = parts
                elif len(parts) == 4:
                    protocol, local_addr, foreign_addr, state = parts
                    pid = ''
                if protocol == "UDP":
                    state = ""
                program_name = NO_PERMISSION_STRING[1] if current_program.strip() == NO_PERMISSION_STRING[
                    0] else current_program.strip()
                program_name = EMPTY_STRING[1] if program_name.strip() == EMPTY_STRING[0] else program_name.strip()

                if program_name != NO_PERMISSION_STRING[1]:
                    if not self.is_private_ip(foreign_addr):
                        if program_name not in self.program_names:
                            self.program_names[program_name] = True

                connections.append((protocol, local_addr, foreign_addr, state, pid, program_name))
                current_program = ''
            else:
                current_program = line.replace('[', '').replace(']', '')

        return connections

    def is_private_ip(self, ip):
        ip = validate_and_expand_ip(extract_ip(ip))
        try:
            ip_obj = ipaddress.ip_address(ip)
            is_private = ip_obj.is_private
            if not is_private:
                self.external_ips.append(ip)
            return is_private
        except ValueError:
            return False

    def calculate_abuse_color(self, abuse_score):
        start_color = '#23BC82'
        end_color = '#A52E6A'
        # Calculate color based on abuse score (0-100)
        # Interpolate between start_color and end_color using abuse score
        if abuse_score < 0:
            abuse_score = 0
        elif abuse_score > 100:
            abuse_score = 100

        # Extract RGB components from start_color
        start_r = int(start_color[1:3], 16)
        start_g = int(start_color[3:5], 16)
        start_b = int(start_color[5:7], 16)

        # Extract RGB components from end_color
        end_r = int(end_color[1:3], 16)
        end_g = int(end_color[3:5], 16)
        end_b = int(end_color[5:7], 16)

        # Interpolate between start_color and end_color using abuse score
        r = math.ceil(start_r + (end_r - start_r) * (abuse_score / 100))
        g = math.ceil(start_g + (end_g - start_g) * (abuse_score / 100))
        b = math.ceil(start_b + (end_b - start_b) * (abuse_score / 100))

        # Convert RGB values to hex format
        color = f'#{r:02X}{g:02X}{b:02X}'
        return color

    def send_external_ips(self, selected_ips, result_tree):
        clients = [AbuseIPDB(), IpApiCom()]
        selected_ips = [validate_and_expand_ip(extract_ip(ip)) for ip in selected_ips]
        for client in clients:
            if client.api_key == False:
                continue
            if selected_ips:
                info = client.batch_get_ip_info(selected_ips)
                if info:
                    for ip_info in info:
                        isp = ip_info.get('ISP', '')
                        country = ip_info.get('Country', '')
                        abuse = ip_info.get('Abuse', '')

                        # Calculate color for abuse score
                        if abuse:
                            abuse_color = self.calculate_abuse_color(int(abuse))
                        else:
                            abuse_color = None

                        for item in result_tree.get_children():
                            values = result_tree.item(item, 'values')
                            treeview_ip = validate_and_expand_ip(extract_ip(values[2]))
                            if treeview_ip == validate_and_expand_ip(ip_info['IP']):
                                result_tree.item(item, values=(
                                    values[0], values[1], values[2], values[3], values[4], values[5], isp, country,
                                    abuse), tags=('abuse_color',))
                                result_tree.tag_configure('abuse_color', foreground=abuse_color)

                    messagebox.showinfo("Info", "External IPs have been sent.")
                    break
                else:
                    messagebox.showerror("Error", "Failed to fetch IP information.")
            else:
                messagebox.showwarning("Warning", "No external IPs selected.")
