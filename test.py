import argparse
import os

import dbus


def get_brightness(device_id, format="percentage"):
    # Path to the backlight device
    backlight_path = f"/sys/class/backlight/{device_id}/"

    # Get the current and maximum brightness levels
    with open(os.path.join(backlight_path, "brightness"), "r") as f:
        brightness = float(f.read().strip())

    with open(os.path.join(backlight_path, "max_brightness"), "r") as f:
        max_brightness = float(f.read().strip())

    if format == "percentage":
        percentage = round((brightness / max_brightness) * 100)
        return percentage
    elif format == "raw":
        return int(brightness)


def set_brightness(device_id, value):
    # Path to the backlight device
    backlight_path = f"/sys/class/backlight/{device_id}/"

    # Get the maximum brightness
    with open(os.path.join(backlight_path, "max_brightness"), "r") as f:
        max_brightness = float(f.read().strip())

    # Determine if value is percentage or raw value
    if "%" in value:
        desired_percentage = float(value.strip("%"))
        desired_brightness = (desired_percentage / 100.0) * max_brightness
    else:
        desired_brightness = float(value)

    # Round the brightness value properly
    desired_brightness = round(desired_brightness)

    # Connect to the system bus
    bus = dbus.SystemBus()

    # Get a proxy object for the login1 session
    proxy = bus.get_object(
        "org.freedesktop.login1", "/org/freedesktop/login1/session/auto"
    )

    # Get the interface for the Session
    interface = dbus.Interface(proxy, "org.freedesktop.login1.Session")

    # Call the SetBrightness method with the calculated brightness value
    interface.SetBrightness("backlight", device_id, dbus.UInt32(desired_brightness))

    print(f"Set brightness to {desired_brightness} (out of {int(max_brightness)})")


def main():
    parser = argparse.ArgumentParser(
        description="Get or set the screen brightness for a specified backlight device."
    )

    # Subcommands: get and set
    subparsers = parser.add_subparsers(dest="command")

    # 'set' subcommand
    set_parser = subparsers.add_parser("set", help="Set the brightness level.")
    set_parser.add_argument(
        "value", type=str, help="Brightness level (percentage or raw value)."
    )
    set_parser.add_argument(
        "--device",
        type=str,
        default="amdgpu_bl1",
        help="The backlight device ID (default: amdgpu_bl1)",
    )

    # 'get' subcommand
    get_parser = subparsers.add_parser("get", help="Get the current brightness level.")
    get_parser.add_argument(
        "--format",
        type=str,
        choices=["percentage", "raw"],
        default="percentage",
        help="Output format: percentage (default) or raw value.",
    )
    get_parser.add_argument(
        "--device",
        type=str,
        default="amdgpu_bl1",
        help="The backlight device ID (default: amdgpu_bl1)",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "set":
        set_brightness(args.device, args.value)
    elif args.command == "get":
        brightness = get_brightness(args.device, args.format)
        if args.format == "percentage":
            print(f"Brightness: {brightness}%")
        else:
            print(f"Brightness: {brightness} (raw value)")


if __name__ == "__main__":
    main()
