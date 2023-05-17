import time
import sys

def print_colorful(text, color, *args, **kwargs):
    color_code = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m"
    }

    reset_code = "\033[0m"

    if color and color in color_code:
        colored_text = color_code[color] + str(text) + reset_code
        print(colored_text, *args, **kwargs)
    else:
        print(text, *args, **kwargs)


def sleep_with_progress(duration):
    total_ticks = 30
    tick_interval = duration / total_ticks

    for i in range(total_ticks):
        elapsed_seconds = round((i + 1) * tick_interval, 2)
        sys.stdout.write(f"\rTime elapsed: {elapsed_seconds} second(s) ")
        sys.stdout.flush()
        time.sleep(tick_interval)

    sys.stdout.write("\n")


def files_checked_progress(number):

    if number == 1:
        sys.stdout.flush()
    sys.stdout.write(f"\rFiles Checked: {number}")

