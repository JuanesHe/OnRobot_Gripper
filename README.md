# OnRobot_Gripper

Python library and example scripts to manage **OnRobot 2FG7** and **3FG15** grippers over **Modbus TCP**.

## Repository contents

- `control_Onrobot.py` – reusable classes for controlling the grippers
- `search.py` – scans Modbus unit IDs to find responding devices
- `test.py` – low-level register read/write test script

## Requirements

- Python 3.9+
- Network access to the OnRobot Compute Box
- `pymodbus`

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Update the IP address and unit IDs in the scripts to match your setup.

Default values currently used in the examples:

- IP: `192.168.1.1`
- 3FG15 unit ID: `66`
- 2FG7 unit ID: `67`

## Usage

Run the main control example:

```bash
python control_Onrobot.py
```

Scan unit IDs:

```bash
python search.py
```

Run the low-level test script:

```bash
python test.py
```

## Notes

- The scripts communicate using Modbus TCP on port `502`.
- Register mappings and scaling are based on the current implementation in this repository.
- Test carefully on real hardware before using in production workflows.
