"""Color utilities for terminal"""

import os
import sys

if sys.platform == "win32":
    import colorama
    colorama.init()

COLORS_SUPPORTED = (
    hasattr(sys.stdout, 'isatty') and 
    sys.stdout.isatty() and 
    os.name != 'nt' or os.environ.get('TERM') == 'xterm-256color'
)

class Colors:
    """ANSI color codes"""
    BLUE = '\033[94m' if COLORS_SUPPORTED else ''
    GREEN = '\033[92m' if COLORS_SUPPORTED else ''
    YELLOW = '\033[93m' if COLORS_SUPPORTED else ''
    RED = '\033[91m' if COLORS_SUPPORTED else ''
    PURPLE = '\033[95m' if COLORS_SUPPORTED else ''
    CYAN = '\033[96m' if COLORS_SUPPORTED else ''
    GRAY = '\033[90m' if COLORS_SUPPORTED else ''
    BOLD = '\033[1m' if COLORS_SUPPORTED else ''
    RESET = '\033[0m' if COLORS_SUPPORTED else ''

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
║                               👁️  N X - T R A C E  👁️                                                ║
║                             Network Security Scanner v2.0.0                                           ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

# Funções de output
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