import ipaddress
import re

def validate_and_expand_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv6Address):
            # Expand the abbreviated IPv6 address to its full form
            full_address = ip_obj.exploded
        else:
            # For IPv4, just return the address as it doesn't have an abbreviated form
            full_address = str(ip_obj)
        return full_address
    except ValueError:
        return None

def extract_ip(address):
    # Pattern to match IPv6 addresses with optional port in square brackets
    ipv6_pattern = re.compile(
        r'\[([^\]]+)\]|([^:]+:[^:]+:[^:]+:[^:]+:[^:]+:[^:]+:[^:]+:[^:]+)|([^:]+:[^:]+:[^:]+:[^:]+:[^:]+:[^:]+:[^:]+)')

    # Pattern to match IPv4 addresses with optional port
    ipv4_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)')

    # Check if the address matches the IPv6 pattern
    match = ipv6_pattern.match(address)
    if match:
        return match.group(1) if match.group(1) else match.group(0)

    # Check if the address matches the IPv4 pattern
    match = ipv4_pattern.match(address)
    if match:
        return match.group(1)
    return None