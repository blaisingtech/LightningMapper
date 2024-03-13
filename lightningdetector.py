import smbus
import time

class AS3935:
    def __init__(self, address, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.init_sensor()

    def write_register(self, register, value):
        self.bus.write_byte_data(self.address, register, value)

    def read_register(self, register):
        return self.bus.read_byte_data(self.address, register)

    def init_sensor(self):
        # Reset the sensor to its default state
        self.write_register(0x3C, 0x96)
        time.sleep(0.002)  # Wait for reset to complete
        
        # Set the noise floor level and other initialization settings as needed
        # Noise floor level to its default or a specific setting based on your environment
        self.write_register(0x01, 0x24)  # Example setting, adjust as necessary

        # Calibrate the oscillators
        self.write_register(0x3D, 0x96)

    def read_lightning_distance(self):
        # This method returns the distance to the storm front if lightning is detected
        distance = self.read_register(0x07)
        return distance

    def read_lightning_energy(self):
        # This method returns the energy of the lightning strike
        msb = self.read_register(0x06)
        mid = self.read_register(0x05)
        lsb = self.read_register(0x04)
        return (msb << 16) | (mid << 8) | lsb

    def check_lightning(self):
        # Check if there is an interrupt for a lightning event
        interrupt_reg = self.read_register(0x03)
        if interrupt_reg & 0x08:  # Lightning interrupt
            return True
        return False

# Example usage
if __name__ == "__main__":
    sensor_address = 0x03  # Adjust to your sensor's I²C address
    as3935 = AS3935(sensor_address)

    if as3935.check_lightning():
        distance = as3935.read_lightning_distance()
        energy = as3935.read_lightning_energy()
        print(f"Lightning detected! Distance: {distance} km, Energy: {energy}")
    else:
        print("No lightning detected.")
