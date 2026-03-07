"""Input validators"""

import re
from urllib.parse import urlparse
from typing import Optional

def validate_target(target: str) -> str:
    """Validates and nomalizes target URL"""
    if not target:
        raise ValueError("Target cannot be empty")
    
    # Add scheme if missing
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    # Validade URL Format
    parsed = urlparse(target)
    if not parsed.netloc:
        raise ValueError(f"Invalid target URL: {target}")
    
    # Remove trailing slash
    return target.rstrip('/')

def validate_port(port: Optional[int]) -> Optional[int]:
    """Validates port number"""
    if port is None:
        return None
    
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}. Must be between 1 and 65535")
    
    return port

def validate_timeout(timeout: int) -> int:
    """Validate timeout value"""
    if timeout < 1:
        raise ValueError("Timeout must be at least 1 second")
    if timeout > 300:
        raise ValueError("Timeout cannot exceed 300 seconds (5 minutes)")
    return timeout