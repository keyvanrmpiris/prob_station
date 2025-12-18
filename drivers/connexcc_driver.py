import serial
import time
import ctypes
from pathlib import Path
import os

# 1. Define the path to your 'lib' folder relative to the script root
# This gets the directory where your script is located
root_dir = Path(__file__).parent.parent.absolute()
lib_path = root_dir / "libs"
print(f"conexcc lib path is: {lib_path}")

# 2. Add the directory to the DLL search path
if os.path.exists(lib_path):
    os.add_dll_directory(str(lib_path))
    print(f"Added to DLL search path: {lib_path}")

# 3. Load the specific DLL
try:
    # Replace 'your_library.dll' with your actual file name
    my_lib = ctypes.CDLL("Newport.CONEXCC.CommandInterface.dll") 
    print("DLL loaded successfully!")
except OSError as e:
    print(f"Failed to load DLL: {e}")


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
                controller = serial.Serial(
                    port=port,
                    baudrate=921600,
                    timeout=1 # Ensure timeout is set for readline()
                )
                
                # Verification Handshake
                controller.write(b'1VE\r\n')
                response = controller.readline().decode('utf-8').strip()
                
                if "CONEX-CC" in response:
                    print(f"Successfully verified CONEX-CC on {port}")
                    self.controller.append(controller)
                else:
                    print(f"Port {port} opened, but device did not identify as CONEX-CC.")
                    controller.close()

            except serial.SerialException as e:
                print(f"Could not open {port}: {e}")
    def send_command(self, command="", controller_id = 0, device_id=1):
        """Sends an ASCII command and reads the response."""
        # Commands must be terminated with CRLF (\r\n)
        full_command = f"{device_id}{command}\r\n"
        print(controller_id)
        self.controller[controller_id].write(full_command.encode('utf-8'))
        time.sleep(0.1) # Wait briefly for response
        # Read all lines in buffer
        response = self.controller[controller_id].read_all().decode('utf-8').strip()
        return response