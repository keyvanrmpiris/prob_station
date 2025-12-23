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
import threading

class Rigol:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.resources = self.rm.list_resources()
        if not self.resources:
            raise Exception("No VISA resources found.")
        print(f"Target Resource: {self.resources[0]}")
        self.SCOPE_ADDRESS = self.resources[0] 
        self.scope = None
        self.keep_running = False # Flag for the loop
        self.scale = 1
        self.offset = 0
        self.status_string = None

    def connect(self):
        try:
            self.scope = self.rm.open_resource(self.SCOPE_ADDRESS)
            # Standard IDN query to verify connection
            print(f"Connected to: {self.scope.query('*IDN?').strip()}") 
        except pyvisa.errors.VisaIOError as e:
            print(f"VISA Error: {e}")

    def set_vertical_scale(self, channel=1, volts_per_div=0.1):
        """
        Sets the vertical scale for a specific channel.
        To see a 5V peak-to-peak signal clearly 1v (1V) is recommended.
        """
        try:
            # Example: :CHANnel1:SCALe 0.2
            self.scope.write(f':CHANnel{channel}:SCALe {volts_per_div}')
            print(f"Channel {channel} scale set to {volts_per_div}V/div")

            self.scope.write(f':CHANnel{channel}:OFFSet {self.offset}')
            print(f"Channel {channel} offset set to {self.offset}V")
        except Exception as e:
            print(f"Error setting scale: {e}")

    def get_vertical_params(self, channel=1):
        """
        Returns the current scale and offset for a channel.
        Useful for manual voltage calculations.
        """
        try:
            self.scale = float(self.scope.query(f':CHANnel{channel}:SCALe?'))
            self.offset = float(self.scope.query(f':CHANnel{channel}:OFFSet?'))
            output = f"Ch{channel} Config: {self.scale} V/div, {self.offset} V Offset"
            return output
        except Exception as e:
            print(f"Error reading scale: {e}")
            

    def _loop_logic(self):
        """Internal method that runs in a background thread."""
        print("\n--- Starting Continuous Read (5ms) ---")
        print("--- Press ENTER in the console to stop ---\n")
        
        self.scope.write(':MEASure:STATistic:ITEM VPP,CHANnel1')
        raw_val=0
        while self.keep_running:
            try:
                vertical_params_print = self.get_vertical_params()
                raw_val = self.scope.query(':MEASure:STATistic:ITEM? AVERages,VPP,CHANnel1').strip()
                # Convert to float to handle scientific notation
                vpp_value = float(raw_val)
                true_val = (vpp_value-self.offset)*self.scale
                # Format the output: 
                # :.4f keeps it to 4 decimal places
                # <20 pads the string to 20 characters so it overwrites old text
                output = f" [LIVE] Vpp: {true_val:.4f} V | {vertical_params_print}"
                
                self.status_string = output
                
                time.sleep(0.05)
            except Exception as e:
                # If the scope returns "9.9e37" (Out of Range), handle it gracefully
                print(e)
                print(f"\rError/Out of Range: {raw_val:<30}", end='')
                print(f"\rError/Out of Range: {true_val:<30}", end='')
                time.sleep(0.05)
    def get_trigger_source(self):
        """
        Queries the scope to find out which channel is the trigger source.
        Returns strings like 'CHAN1', 'CHAN2', 'EXT', or 'ACLine'.
        """
        try:
            source = self.scope.query(':TRIGger:EDGE:SOURce?').strip()
            print(f"Current Trigger Source: {source}")
            return source
        except Exception as e:
            print(f"Error reading trigger source: {e}")
            return None

    def get_status(self):
        """Helper to safely get the string"""
        return getattr(self, 'status_string', "Initializing...")
        
    # def monitor_measurements(self):
    #     """Starts the 50ms read loop and waits for user input to stop."""
    #     self.keep_running = True
        
    #     # Start the background thread
    #     thread = threading.Thread(target=self._loop_logic)
    #     thread.daemon = True
    #     thread.start()

    #     # Block the main thread here until user presses Enter
    #     input() 
        
    #     # Signal the thread to stop
    #     self.keep_running = False
    #     thread.join()
    #     print("\nMonitoring stopped.")

    def monitor_measurements(self):
        """Starts the background loop and returns control to the main program immediately."""
        if not hasattr(self, 'keep_running') or not self.keep_running:
            self.keep_running = True
            # We store the thread as an attribute (self.thread) so we can join it later
            self.thread = threading.Thread(target=self._loop_logic)
            self.thread.daemon = True
            self.thread.start()
            print("\n[Rigol] Background monitoring active.")
        else:
            print("\n[Rigol] Monitoring is already running.")

    def stop_monitoring(self):
        """Properly shuts down the background thread."""
        self.keep_running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=1.0)
            print("\n[Rigol] Monitoring stopped.")

    def disconnect(self):
        if self.scope:
            self.scope.close()
            print("Scope disconnected.")
