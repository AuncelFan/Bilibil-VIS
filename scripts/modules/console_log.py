RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"


def LOG(s, type="LOG", color=RESET):
    print(f"{color}[{type}]{RESET} {s}")


def INFO(s):
    LOG(s, "INFO", GREEN)


def PROC(s):
    LOG(s, "PROC", BLUE)


def WARN(s):
    LOG(s, "WARN", YELLOW)


def ERROR(s):
    LOG(s, "ERROR", RED)