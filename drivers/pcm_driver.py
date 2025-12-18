import sys
import os
import inspect
import ctypes
# Import the .NET Common Language Runtime (CLR) to allow interaction with .NET
import clr
import numpy as np
import time # Added for potential use, though not strictly required
from pathlib import Path
from System.Text import StringBuilder

# 1. Setup Paths
root_dir = Path(__file__).parent.parent.absolute()
lib_path = root_dir / "libs"

# Add to Python path so 'clr' can find the .NET DLLs
if str(lib_path) not in sys.path:
    sys.path.append(str(lib_path))

# Add to DLL Search path so Windows can find the underlying USB C++ DLLs
if os.path.exists(lib_path):
    os.add_dll_directory(str(lib_path))

# 2. Add References (DO NOT use ctypes.CDLL for these)
try:
    # clr.AddReference searches sys.path for the filename provided
    clr.AddReference("DeviceIOLib")
    clr.AddReference("CmdLib8742")
    print("Assemblies loaded successfully!")
    
    # Now you can import the namespaces inside the DLLs
    from Newport.DeviceIOLib import *
    from NewFocus.PicomotorApp import CmdLib8742
    print("Imports successful!")

except Exception as e:
    print(f"Failed to load assemblies: {e}")
    # This often happens if UsbDllWrap.dll is missing from the libs folder

class Pcm:
    def __init__(self):
        

        print ("Waiting for device discovery...")
        # Call the class constructor to create an object
        self.deviceIO = DeviceIOLib (True)
        self.cmdLib8742 = CmdLib8742 (self.deviceIO)

        # Set up USB to only discover picomotors (Controller model 8742)
        self.deviceIO.SetUSBProductID (0x4000)
        self.strDeviceKeys = np.array ([])
        self.nDeviceCount = 0
        self.picomotor_map = {} # Maps 'L' or 'R' to the actual device key (serial number)
        self.open_device_keys = [] # List to track all successfully opened devices

        self.strBldr = StringBuilder (64)
        self.nReturn = -1

    def connect(self):
        # Discover USB and Ethernet devices - delay 5 seconds
        self.deviceIO.DiscoverDevices (5, 5000)

        # Get the list of discovered devices
        
        self.strDeviceKeys = self.deviceIO.GetDeviceKeys ()
        self.nDeviceCount = self.deviceIO.GetDeviceCount ()
        print ("Device Count = %d\n" % self.nDeviceCount)

        # --- New Logic for Looping Command Input ---
        

        if (self.nDeviceCount > 0) :
            n = 0
            # First, open all devices and map their keys based on the serial number
            for oDeviceKey in self.strDeviceKeys :
                strDeviceKey = str (oDeviceKey)
                n = n + 1
                print (f"Device Key[{n}] = {strDeviceKey}")

                # If the device was opened
                if (self.deviceIO.Open (strDeviceKey)) :
                    self.open_device_keys.append(strDeviceKey)
                    
                    # Identify the instrument to get the serial number
                    strModel = ""
                    strSerialNum = ""
                    strFwVersion = ""
                    strFwDate = ""
                    
                    # The IdentifyInstrument method is used to retrieve instrument details
                    strModel, strSerialNum, strFwVersion, strFwDate = self.cmdLib8742.IdentifyInstrument (strDeviceKey, strModel, strSerialNum, strFwVersion, strFwDate)
                    
                    # Map the device key based on the serial number
                    if (strSerialNum == "105969") :
                        print (f"-> Mapped as 'L' (Serial: {strSerialNum})")
                        self.picomotor_map['L'] = strDeviceKey
                    elif (strSerialNum == "105970") :
                        print (f"-> Mapped as 'R' (Serial: {strSerialNum})")
                        self.picomotor_map['R'] = strDeviceKey
                    else:
                        print (f"-> Found device with serial {strSerialNum} but not mapped (not 105969 or 105970).")

                    print (f"Model = {strModel}")
                    print (f"Serial Num = {strSerialNum}")
                    print (f"Fw Version = {strFwVersion}")
                    print (f"Fw Date = {strFwDate}\n")

    def send_command(self, cmd=""):

        if (self.nDeviceCount > 0) :
            # --- Start main loop to accept user commands ---
            if 'L' in self.picomotor_map or 'R' in self.picomotor_map:
                print("\n--- Picomotor Control Interface ---")
                print("Enter a command (e.g., 'L3PR1000' or 'RREL-500').")
                print("The first character (L/R) selects the motor, the rest is the command.")
                print("Type 'Q' or 'QUIT' to exit.")
                
                while True:
                    try:
                        # Note: 'input()' is for Python 3. For Python 2, use 'raw_input()'.
                        user_input = input("Command (L/R + Cmd): ").strip()
                        
                        if not user_input:
                            continue

                        if user_input.upper() in ["Q", "QUIT"]:
                            print("Exiting command loop...")
                            break
                        
                        if len(user_input) < 2:
                            print("Error: Command too short. Format is [L/R][Command]")
                            continue

                        # The first character is the target ('L' or 'R')
                        target_key = user_input[0].upper()
                        # The rest is the command string
                        command = user_input[1:]
                        
                        if target_key in self.picomotor_map:
                            device_key_to_use = self.picomotor_map[target_key]
                            
                            print(f"Sending command '{command}' to device '{target_key}' ({device_key_to_use})...")
                            
                            # Send the command using deviceIO.Query
                            self.strBldr.Remove (0, self.strBldr.Length)
                            # For a simple command (like a move command), deviceIO.Write may be used,
                            # but Query allows for command confirmation or error messages.
                            nReturn = self.deviceIO.Query (device_key_to_use, command, self.strBldr)
                            
                            print (f"Return Status = {self.nReturn}")
                            print (f"Response = {self.strBldr.ToString ()}\n")
                            
                        else:
                            print(f"Error: Invalid target key '{target_key}'. Available keys: {', '.join(self.picomotor_map.keys())}.")
                            
                    except EOFError:
                        print("\nEOF received. Exiting loop...")
                        break
                    except Exception as e:
                        print(f"An error occurred in the command loop: {e}")
                        time.sleep(0.1) # Prevents fast looping on repeated errors
                        
            else:
                print ("No target devices ('105969' or '105970') were discovered and mapped for control.\n")
            
        else :
            print ("no device to operate.\n")

    def close_connection(self):
        print("Shutting down and closing all open devices...")
        for key in self.open_device_keys:
            self.nReturn = self.deviceIO.Close (key)
            print(f"Closed device {key}. Status: {nReturn}")
        # Shut down all communication
        self.cmdLib8742.Shutdown ()
        self.deviceIO.Shutdown ()
        print ("Communication Shutdown complete.")