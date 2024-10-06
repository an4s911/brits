# Brits - A Simple Linux Brightness Control Script

`brits` is a Python script to get and set the screen brightness on Linux systems using the DBus interface. It supports retrieving the brightness in both percentage and raw values, as well as setting brightness via raw values or percentages, with options to increment or decrement.

## Features

- **Get Brightness**:
  - Get current brightness as a percentage (default).
  - Get current brightness as a raw value.
  
- **Set Brightness**:
  - Set brightness using raw values (e.g., `200`).
  - Set brightness using percentage values (e.g., `60%`).
  - Increment or decrement brightness using either raw values or percentages (e.g., `20+`, `10%-`).

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/an4s911/brits.git
    cd brits
    ```

2. **Install dependencies:**
    - Make sure you have `dbus-python` installed:
    ```bash
    pip install dbus-python
    ```

3. **Make the script executable:**
    ```bash
    chmod +x brits.py
    ```

4. **(Optional)**: You can add the script to your PATH for easier access:
    ```bash
    sudo cp brits.py /usr/local/bin/brits
    ```

## Usage

### Get Brightness

- **Default (percentage):**
    ```bash
    brits get
    ```
  
- **Get brightness as percentage explicitly:**
    ```bash
    brits get --percentage
    ```

- **Get raw brightness value:**
    ```bash
    brits get --raw
    ```

### Set Brightness

- **Set brightness to a raw value:**
    ```bash
    brits set 200
    ```

- **Set brightness to a percentage:**
    ```bash
    brits set 60%
    ```

- **Increase brightness by a raw value:**
    ```bash
    brits set 20+
    ```

- **Decrease brightness by a percentage:**
    ```bash
    brits set 10%-
    ```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository, create a new branch for your changes, and submit a pull request. Thank you for your interest in improving this project!
