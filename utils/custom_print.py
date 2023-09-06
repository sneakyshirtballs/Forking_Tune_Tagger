import sys, time

# ANSI escape codes for text colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def p_status(message, delay=0):
    print(f"[INFO] {message}")
    time.sleep(delay)

def p_terminate(message, delay=0):
    print(f"{RED}[ERROR] {message}{RESET}")
    time.sleep(delay)
    sys.exit(1)

def p_success(message, delay=0):
    print(f"{GREEN}[SUCCESS] {message}{RESET}")
    time.sleep(delay)

def p_warning(message, delay=0):
    print(f"{YELLOW}[WARNING] {message}{RESET}")
    time.sleep(delay)
