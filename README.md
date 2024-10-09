# Brits - A Simple Linux Brightness Control Script

`brits` is a Python script to get and set the screen brightness on Linux systems. It supports retrieving the brightness in both percentage and raw values, as well as setting brightness via raw values or percentages, with options to increment or decrement.

## Features

- **Get Brightness**:
  - Get current brightness as a percentage (default).
  - Get current brightness as a raw value.
  
- **Set Brightness**:
  - Set brightness using raw values (e.g., `200`).
  - Set brightness using percentage values (e.g., `60%`).
  - Increment or decrement brightness using either raw values or percentages (e.g., `20+`, `10%-`).
 
## Motivation

I was using `brightnessctl`, but it didn't always give me the proper percentage values, which was a bit annoying. So, I decided to build my own tool in Python instead. I checked out the source code of `brightnessctl` and found that it uses DBus, so I ported that functionality into Python initially, but now I've updated it and it doesn't use DBus anymore. Now, `brits` gives accurate percentage values and works just how I wanted it to!

## Installation

### Dependencies
\**the only dependency is `python3`.*

1. **Clone the repository:**
    ```bash
    git clone https://github.com/an4s911/brits.git
    cd brits
    ```

2. **Make the script executable:**
    ```bash
    chmod +x brits.py
    ```

3. **(Optional)**: You can add the script to your PATH for easier access:
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
    brits get p[ercentage] 
    ```

- **Get raw brightness value:**
    ```bash
    brits get r[aw]
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
