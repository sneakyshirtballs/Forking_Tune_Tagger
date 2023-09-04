import sys

# ANSI escape codes for text colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def p_status(message):
    print(f"[INFO] {message}")

def p_terminate(message):
    print(f"{RED}[ERROR] {message}{RESET}")
    sys.exit(1)

def p_success(message):
    print(f"{GREEN}[SUCCESS] {message}{RESET}")

def p_warning(message):
    print(f"{YELLOW}[WARNING] {message}{RESET}")
