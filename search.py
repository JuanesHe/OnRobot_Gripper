from pymodbus.client import ModbusTcpClient
import time


IP = "192.168.1.1"
PORT = 502

REGISTER_TO_TEST = 256  # status register (common OnRobot convention)


def test_unit_id(client, unit_id):
    try:
        result = client.read_holding_registers(
            address=REGISTER_TO_TEST,
            count=1,
            slave=unit_id
        )

        if result is None:
            return None

        if hasattr(result, "registers"):
            return result.registers[0]

    except Exception:
        return None

    return None


def main():
    client = ModbusTcpClient(IP, port=PORT)

    if not client.connect():
        print("Cannot connect to Compute Box")
        return

    print(f"Connected to {IP}:{PORT}")
    print("Scanning Unit IDs 1–255...\n")

    found = []

    for unit_id in range(1, 256):

        value = test_unit_id(client, unit_id)

        if value is not None:
            print(f"✔ Unit ID {unit_id:3d} → Register {REGISTER_TO_TEST} = {value}")
            found.append((unit_id, value))
        else:
            print(f"— Unit ID {unit_id:3d} no response")

        time.sleep(0.05)  # small delay to avoid flooding

    client.close()

    print("\n=== SUMMARY ===")
    if not found:
        print("No devices responded.")
    else:
        print(f"Found {len(found)} responding unit IDs:")
        for uid, val in found:
            print(f"  - Unit ID {uid} → status={val}")


if __name__ == "__main__":
    main()
