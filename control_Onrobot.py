from pymodbus.client import ModbusTcpClient
import time

class OnRobotGripper:
    def __init__(self, ip, unit_id):
        self.client = ModbusTcpClient(ip, port=502)
        self.unit_id = unit_id

        if not self.client.connect():
            raise Exception(f"Cannot connect to {ip}")

    def write_reg(self, address, value):
        self.client.write_register(
            address=address,
            value=value,
            device_id=self.unit_id
        )

    def read_reg(self, address):
        result = self.client.read_holding_registers(
            address=address,
            count=1,
            device_id=self.unit_id
        )
        
        if result.isError():
             raise Exception(f"Modbus error reading register {address} on Unit {self.unit_id}")

        return result.registers[0]

    def wait_until_ready(self):
        while True:
            # Register 256 is the Status block
            status = self.read_reg(256)
            busy = status & 0x01

            if busy == 0:
                break
            
            time.sleep(0.1)

    def get_position_internal_mm(self):
        # Register 257 stores the live physical Width/Diameter 
        raw_value = self.read_reg(257)
        return raw_value / 10.0

    def get_position_external_mm(self):
        # Register 258 stores the live physical Force being applied
        raw_value = self.read_reg(258)
        return raw_value / 10.0

    def disconnect(self):
        self.client.close()


class Gripper3FG15(OnRobotGripper):
    # 3FG15 4-Register Map
    REG_FORCE = 0
    REG_DIAMETER = 1
    REG_GRIP_TYPE = 2
    REG_CONTROL = 3

    CMD_GRIP = 1
    CMD_STOP = 4

    EXTERNAL_GRIP = 0
    INTERNAL_GRIP = 1

    def grip(self, diameter_mm, force_n, internal=False):
        target_diameter = int(diameter_mm * 10)
        target_force = int(force_n * 10)

        self.write_reg(self.REG_FORCE, target_force)
        self.write_reg(self.REG_DIAMETER, target_diameter)

        grip_type = self.INTERNAL_GRIP if internal else self.EXTERNAL_GRIP
        self.write_reg(self.REG_GRIP_TYPE, grip_type)

        self.write_reg(self.REG_CONTROL, self.CMD_GRIP)
        self.wait_until_ready()

    def stop(self):
        self.write_reg(self.REG_CONTROL, self.CMD_STOP)


class Gripper2FG7(OnRobotGripper):
    # 2FG7 3-Register Map
    REG_WIDTH = 0
    REG_FORCE = 1
    REG_GRIP_TYPE = 2
    REG_CONTROL = 3  

    CMD_GRIP = 1
    CMD_STOP = 4

    EXTERNAL_GRIP = 0
    INTERNAL_GRIP = 1


    def grip(self, width_mm, force_n, internal=False):
        target_width = int(width_mm * 10)
        target_force = int(force_n * 10)

        self.write_reg(self.REG_FORCE, target_force)
        self.write_reg(self.REG_WIDTH, target_width)

        grip_type = self.INTERNAL_GRIP if internal else self.EXTERNAL_GRIP
        self.write_reg(self.REG_GRIP_TYPE, grip_type)

        self.write_reg(self.REG_CONTROL, self.CMD_GRIP)
        self.wait_until_ready()

    def stop(self):
        self.write_reg(self.REG_CONTROL, self.CMD_STOP)


# -------------------------------------------------------
# Execution Sequence
# -------------------------------------------------------
if __name__ == "__main__":
    IP = "192.168.1.1"

    # From your setup
    UNIT_ID_3FG15 = 66
    UNIT_ID_2FG7 = 67

    gripper_3fg15 = Gripper3FG15(IP, UNIT_ID_3FG15)
    gripper_2fg7 = Gripper2FG7(IP, UNIT_ID_2FG7)

    try:
        # --- 3FG15 Sequence ---
        print(f"Opening 3FG15 to 135mm...")
        gripper_3fg15.grip(diameter_mm=135, force_n=100, internal=False) 
        print(f"> 3FG15 Status | Position: {gripper_3fg15.get_position_internal_mm()} mm | Force: {gripper_3fg15.get_position_external_mm()} mm")
        
        print("Waiting 2 seconds...")
        time.sleep(2.0)
        
        print(f"Closing 3FG15 to 70mm...")
        gripper_3fg15.grip(diameter_mm=70, force_n=100, internal=False) 
        print(f"> 3FG15 Status | Position: {gripper_3fg15.get_position_internal_mm()} mm | Force: {gripper_3fg15.get_position_external_mm()} mm")
        
        print("3FG15 sequence complete.\n")
        time.sleep(1.0)

        # --- 2FG7 Sequence ---
        print(f"Opening 2FG7 to 70mm...")
        gripper_2fg7.grip(width_mm=70, force_n=50,internal=False) 
        print(f"> 2FG7 Status | Position: {gripper_2fg7.get_position_internal_mm()} mm | Force: {gripper_2fg7.get_position_external_mm()} mm")
        
        print("Waiting 2 seconds...")
        time.sleep(2.0)
        
        print(f"Closing 2FG7 to 40mm...")
        gripper_2fg7.grip(width_mm=40, force_n=50, internal=False) 
        print(f"> 2FG7 Status | Position: {gripper_2fg7.get_position_internal_mm()} mm | Force: {gripper_2fg7.get_position_external_mm()} mm")
        
        print("2FG7 sequence complete.\n")
        print("Finished.")

    finally:
        gripper_2fg7.disconnect()
        gripper_3fg15.disconnect()
