from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient("192.168.1.1", port=502)
c.connect()

# 1. Check the Status Register (256)
print (c.read_holding_registers(address=256, count=1, device_id=67).registers)
print (c.read_holding_registers(address=257, count=1, device_id=67).registers)
print (c.read_holding_registers(address=258, count=1, device_id=67).registers)
print (c.read_holding_registers(address=259, count=1, device_id=67).registers)
print (c.read_holding_registers(address=260, count=1, device_id=67).registers)
print (c.read_holding_registers(address=261, count=1, device_id=67).registers)
print (c.read_holding_registers(address=262, count=1, device_id=67).registers)
print (c.read_holding_registers(address=263, count=1, device_id=67).registers)
print (c.read_holding_registers(address=264, count=1, device_id=67).registers)
print (c.read_holding_registers(address=265, count=1, device_id=67).registers)
print (c.read_holding_registers(address=266, count=1, device_id=67).registers)
print (c.read_holding_registers(address=267, count=1, device_id=67).registers)
print (c.read_holding_registers(address=268, count=1, device_id=67).registers)

c.write_register(address=0, value=300, device_id=67) #2fg position 
c.write_register(address=1, value=1000, device_id=67) #2fg force
c.write_register(address=2, value=0, device_id=67)
c.write_register(address=3, value=1, device_id=67)


# 1. Check the Status Register (256)
print (c.read_holding_registers(address=258, count=1, device_id=66).registers)


c.write_register(address=0, value=700, device_id=66) #3fg force 
c.write_register(address=1, value=500, device_id=66) #3fg position
c.write_register(address=2, value=0, device_id=66)
c.write_register(address=3, value=1, device_id=66)
