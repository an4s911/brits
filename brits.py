#!/usr/bin/env python3

import os
import re
import sys

BACKLIGHT_DIR = "/sys/class/backlight"
_device = os.listdir(BACKLIGHT_DIR)[0]
MAX_BRIGHTNESS = int(
    open(os.path.join(BACKLIGHT_DIR, _device, "max_brightness")).read().strip()
)
CURRENT_BRIGHTNESS = int(
    open(os.path.join(BACKLIGHT_DIR, _device, "actual_brightness")).read().strip()
)
CURRENT_PERCENTAGE = round((CURRENT_BRIGHTNESS / MAX_BRIGHTNESS) * 100)
BRIGHTNESS_FILE = os.path.join(BACKLIGHT_DIR, _device, "brightness")


def set_raw(value: int):
    value = max(min(value, MAX_BRIGHTNESS), 0)
    with open(BRIGHTNESS_FILE, "w") as f:
        f.write(str(value))


def set_inc_raw(increment: int):
    set_raw(CURRENT_BRIGHTNESS + increment)


def set_dec_raw(decrement: int):
    set_raw(CURRENT_BRIGHTNESS - decrement)


def set_percentage(percentage: int):
    percentage = max(min(percentage, 100), 0)
    value = round((percentage / 100) * MAX_BRIGHTNESS)
    set_raw(value)


def set_inc_percentage(increment: int):
    set_percentage(CURRENT_PERCENTAGE + increment)


def set_dec_percentage(decrement: int):
    set_percentage(CURRENT_PERCENTAGE - decrement)


def parse_set_value(value: str) -> list:
    match = re.match(r"(\d+)(.{0,2})", value)
    value_int = int(match.group(1))
    percentage, plus_minus = sorted(list(match.group(2).ljust(2, "&")))

    is_percentage = percentage == "%"
    is_plus = plus_minus == "+"
    is_minus = plus_minus == "-"

    return value_int, is_percentage, is_plus, is_minus


def set_handler(value: str):
    value_int, is_percentage, is_plus, is_minus = parse_set_value(value)

    if not any([is_percentage, is_plus, is_minus]):
        set_raw(value_int)

    if is_plus:
        if is_percentage:
            set_inc_percentage(value_int)
        else:
            set_inc_raw(value_int)
    elif is_minus:
        if is_percentage:
            set_dec_percentage(value_int)
        else:
            set_dec_raw(value_int)
    elif is_percentage:
        set_percentage(value_int)
    else:
        set_raw(value_int)


def print_help():
    """
    Function to print help message
    """
    help_msg = """
    Usage: brits <command> [options]

    Commands:
        get [p(ercentage)]  Get the current brightness as percentage (default).
        get r(aw)           Get the current brightness as raw value.

        set <value>       Set the brightness to the specified value.
                         Possible values:
                            - 200    (raw value)
                            - 60%    (percentage value)
                            - 20+    (increment raw value)
                            - 30-    (decrement raw value)
                            - 5%+    (increment percentage)
                            - 10%-   (decrement percentage)
    """
    print(help_msg)


def main():
    """
    Main function

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "get":
        if len(sys.argv) == 2 or "percentage".startswith(sys.argv[2]):
            print(f"{CURRENT_PERCENTAGE}%")
        elif "raw".startswith(sys.argv[2]):
            print(CURRENT_BRIGHTNESS)
        else:
            print_help()

    elif command == "set":
        if len(sys.argv) != 3:
            print_help()
            sys.exit(1)

        set_handler(sys.argv[2])

    else:
        print_help()


if __name__ == "__main__":
    main()
