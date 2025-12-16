# from ds1054z import DS1054Z

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

rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print(resources[0])
SCOPE_ADDRESS = resources[0] 

rm = pyvisa.ResourceManager()

try:
    scope = rm.open_resource(SCOPE_ADDRESS)
    print(f"Connected to: {scope.query('*IDN?')}") # Query the device identification

    # Example: Stop the scope acquisition
    scope.write(':STOP')

    # Example: Take a screenshot and save it (requires more complex binary data handling)
    # A dedicated library might be better for screenshots (see below)

    # Example: Read a measurement value (e.g., Vpp of Channel 1)
    scope.write(':MEASure:STATistic:ITEM VPP,CHANnel1')
    time.sleep(1) # Give scope time to measure
    vpp_str = scope.query(':MEASure:STATistic:ITEM? AVERages,VPP,CHANnel1')
    vpp_value = float(vpp_str)
    print(f"Vpp Channel 1 Average: {vpp_value} V")

    # Example: Start the scope acquisition again
    scope.write(':RUN')

    scope.close()

except pyvisa.errors.VisaIOError as e:
    print(f"VISA Error: {e}")
    print("Ensure the scope is connected, powered on, and not in PictBridge mode.")

