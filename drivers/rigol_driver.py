# # Connect using your VISA string or IP address if using LAN
# # The library handles the connection details
# scope = DS1054Z('YOUR_VISA_RESOURCE_STRING') 

# # Save a screenshot to a file
# scope.save_screen("screenshot.png")
# print("Screenshot saved as screenshot.png")

# # Get waveform data
# waveform_data = scope.get_waveform_data(channel=1)
# # You can then use numpy/matplotlib to process/plot this data

# scope.close()


import pyvisa
import time

class Rigol:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.resources = self.rm.list_resources()
        print(self.resources[0])
        self.SCOPE_ADDRESS = self.resources[0] 
        self.scope = None

    def connect(self):
        try:
            scope = self.rm.open_resource(self.SCOPE_ADDRESS)
            print(f"Connected to: {scope.query('*IDN?')}") # Query the device identification
        except pyvisa.errors.VisaIOError as e:
            print(f"VISA Error: {e}")
            print("Ensure the scope is connected, powered on, and not in PictBridge mode.")

    def send_command(self, cmd):
            
            # STOP the scope acquisition again
            self.scope.write(':STOP')
            
            # Example: Take a screenshot and save it (requires more complex binary data handling)
            # A dedicated library might be better for screenshots (see below)

            # Example: Read a measurement value (e.g., Vpp of Channel 1)
            self.scope.write(':MEASure:STATistic:ITEM VPP,CHANnel1')
            time.sleep(1) # Give scope time to measure
            vpp_str = self.scope.query(':MEASure:STATistic:ITEM? AVERages,VPP,CHANnel1')
            vpp_value = float(vpp_str)
            print(f"Vpp Channel 1 Average: {vpp_value} V")

            # Example: Start the scope acquisition again
            self.scope.write(':RUN')

    def disconnect(self):
         self.scope.close()

        
