#!/usr/bin/env python3

import os
import sys

import dbus


def get_brightness_info():
    """
    Function to get the brightness and max brightness values from sysfs

    Returns:
        tuple: A tuple containing the current brightness and max brightness values

    Raises:
        Exception: If there's an error reading the brightness info
    """
    try:
        # Assuming there's only one backlight device
        backlight_dir = "/sys/class/backlight"
        devices = os.listdir(backlight_dir)

        if len(devices) == 0:
            print("No backlight device found.")
            sys.exit(1)

        device = devices[0]
        brightness_file = os.path.join(backlight_dir, device, "brightness")
        max_brightness_file = os.path.join(backlight_dir, device, "max_brightness")

        with open(brightness_file, "r") as f:
            current_brightness = int(f.read().strip())

        with open(max_brightness_file, "r") as f:
            max_brightness = int(f.read().strip())

        return current_brightness, max_brightness, device

    except Exception as e:
        print(f"Error reading brightness info: {e}")
        sys.exit(1)


def set_brightness(device, value):
    """
    Function to set brightness using DBus

    Args:
        device (str): The device to set the brightness for
        value (int): The brightness value to set

    Returns:
        None

    Raises:
        Exception: If there's an error setting the brightness
    """
    try:
        bus = dbus.SystemBus()
        proxy = bus.get_object(
            "org.freedesktop.login1", "/org/freedesktop/login1/session/auto"
        )
        interface = dbus.Interface(proxy, "org.freedesktop.login1.Session")
        interface.SetBrightness("backlight", device, dbus.UInt32(value))
        print(f"Brightness set to {value}.")
    except dbus.DBusException as e:
        print(f"Error setting brightness via DBus: {e}")
        sys.exit(1)


def print_help():
    """
    Function to print help message
    """
    help_msg = """
    Usage: brits <command> [options]

    Commands:
        get               Get the current brightness as percentage (default).
        get --percentage  Get the current brightness as percentage.
        get --raw         Get the current brightness as raw value.

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


def parse_set_value(value, current_brightness, max_brightness):
    """
    Function to parse set value (percentage, raw, increment/decrement)

    Args:
        value (str): The value to parse
        current_brightness (int): The current brightness
        max_brightness (int): The maximum brightness

    Returns:
        int: The parsed value

    Raises:
        ValueError: If the value is invalid
    """
    try:
        if value.endswith("%"):
            percentage = int(value[:-1])
            return int((percentage / 100) * max_brightness)

        elif value.endswith("+") or value.endswith("-"):
            is_percentage = "%" in value
            increment_value = int(value[:-2]) if is_percentage else int(value[:-1])

            if value.endswith("+"):
                if is_percentage:
                    return min(
                        max_brightness,
                        current_brightness
                        + int((increment_value / 100) * max_brightness),
                    )
                else:
                    return min(max_brightness, current_brightness + increment_value)
            elif value.endswith("-"):
                if is_percentage:
                    return max(
                        0,
                        current_brightness
                        - int((increment_value / 100) * max_brightness),
                    )
                else:
                    return max(0, current_brightness - increment_value)

        else:
            return int(value)

    except ValueError:
        print(f"Invalid brightness value: {value}")
        sys.exit(1)


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

    current_brightness, max_brightness, device = get_brightness_info()

    if command == "get":
        if len(sys.argv) == 2 or sys.argv[2] == "--percentage":
            percentage = (current_brightness / max_brightness) * 100
            print(f"Current brightness: {round(percentage)}%")
        elif sys.argv[2] == "--raw":
            print(f"Current brightness: {current_brightness}")
        else:
            print_help()

    elif command == "set":
        if len(sys.argv) < 3:
            print_help()
            sys.exit(1)

        set_value = sys.argv[2]
        new_brightness = parse_set_value(set_value, current_brightness, max_brightness)
        set_brightness(device, new_brightness)

    else:
        print_help()


if __name__ == "__main__":
    main()
