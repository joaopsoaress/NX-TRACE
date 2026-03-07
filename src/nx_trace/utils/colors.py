"""Color utilities for terminal"""

import os
import sys

def supports_color():
    """Check if terminal supports colors"""
    if os.name == 'nt':  # Windows
        # Windows 10+ supports ANSI colors
        return (sys.stdout.isatty() and 
                os.environ.get('TERM') != 'dumb' and
                sys.getwindowsversion().major >= 10)
    else:  # Linux/Mac
        return sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'
    
if sys.platform == "win32":
    import colorama
    colorama.init()

if '--no-color' in sys.argv:
    COLORS_SUPPORTED = False
else:
    COLORS_SUPPORTED = supports_color()

class Colors:
    """ANSI color codes"""
    if COLORS_SUPPORTED:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        GRAY = '\033[90m'
        BOLD = '\033[1m'
        RESET = '\033[0m'
    else:
        BLUE = GREEN = YELLOW = RED = PURPLE = CYAN = GRAY = BOLD = RESET = ''

def print_banner():
    """Print NX ASCII art banner"""
    banner = f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                       ║
║                                  ███╗   ██╗██╗  ██╗                                                   ║
║                                  ████╗  ██║╚██╗██╔╝                                                   ║
║                                  ██╔██╗ ██║ ╚███╔╝                                                    ║
║                                  ██║╚██╗██║ ██╔██╗                                                    ║
║                                  ██║ ╚████║██╔╝ ██╗                                                   ║
║                                  ╚═╝  ╚═══╝╚═╝  ╚═╝                                                   ║
║                                                                                                       ║
║                               👁️  N X - T R A C E  👁️                                                 ║
║                             Network Security Scanner v2.0.0                                           ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

# output functions 
def print_success(text):
    print(f"{Colors.GREEN}[✓]{Colors.RESET} {text}")

def print_error(text):
    print(f"{Colors.RED}[✗]{Colors.RESET} {text}")

def print_info(text):
    print(f"{Colors.BLUE}[i]{Colors.RESET} {text}")

def print_warning(text):
    print(f"{Colors.YELLOW}[!]{Colors.RESET} {text}")

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}[ {text} ]{Colors.RESET}")
    print(f"{Colors.GRAY}─" * 60 + f"{Colors.RESET}")