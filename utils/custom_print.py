import sys

def p_terminate(message):
    print(message)
    sys.exit(1)

def p_status(message):
    print(f"[INFO] {message}")

def p_warning(message):
    print(f"[WARNING] {message}")
