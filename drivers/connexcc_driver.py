import serial
import time

class Conexcc:
    def __init__(self, ports=['COM3','COM4']):
        self.ports = ports
        self.controller = []

    def connect(self):
        """
        Establishes a serial connection to the CONEX-CC controller.
        Adjust the 'port' to match your system's COM port (e.g., 'COM5' on Windows, '/dev/ttyACM0' on Linux).
        """
        for port in self.ports:
            try:
                # The CONEX-CC uses CRLF (\r\n) as command terminators
                controller = serial.Serial(
                    port=port,
                    baudrate=921600, # Default baud rate for USB virtual COM port
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=2, # Read timeout in seconds
                    write_timeout=2
                )
                time.sleep(0.1) # Give the port time to open
                controller.flushInput()
                controller.flushOutput()
                print(f"Connected to {port}")
                self.controller.append(controller)
            except serial.SerialException as e:
                print(f"Error connecting to serial port: {e}")
                return None

    def send_command(self, command="", controller_id=0):
        """Sends an ASCII command and reads the response."""
        # Commands must be terminated with CRLF (\r\n)
        full_command = f"{command}\r\n"
        self.controller[id].write(full_command.encode('utf-8'))
        time.sleep(0.1) # Wait briefly for response
        # Read all lines in buffer
        response = self.controller[id].read_all().decode('utf-8').strip()
        return response

    def main(self):
        # !! IMPORTANT: Change 'COM5' to your controller's actual port !!
        conex = self.connect_conex(port='COM3')

        if conex:
            try:
                # 1. Check the controller state and ID
                # "ID?" queries the device ID
                device_id = self.send_command(conex, "ID?")
                print(f"Device ID: {device_id}")

                # 2. Home the stage (required after power-on)
                # "OR" command initiates the Origin Search
                print("Starting homing sequence (Origin Search)... This may take time.")
                self.send_command(conex, "OR")

                # Wait for homing to complete (check status - "TS" command is useful here)
                # A robust implementation would poll the 'TS' (Status) command, 
                # which returns '33' when moving and '32' or '34' when stopped/ready.
                time.sleep(15) # Simple wait for demo

                # 3. Move to an absolute position
                # "PA10.0" sets the absolute position to 10.0 mm
                target_position = 0.0
                print(f"Moving to absolute position {target_position} mm...")
                self.send_command(conex, f"PA{target_position}")
                time.sleep(5) # Simple wait

                # 4. Get the current position
                # "POS?" queries the current position
                current_pos = self.send_command(conex, "POS?")
                print(f"Current position: {current_pos} mm")

            except Exception as e:
                print(f"An error occurred during communication: {e}")
            finally:
                conex.close()
                print("Connection closed.")