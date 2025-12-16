import sys
import os
import inspect
# Import the .NET Common Language Runtime (CLR) to allow interaction with .NET
import clr
import numpy as np
import time # Added for potential use, though not strictly required

print ("Python %s\n\n" % (sys.version,))

strCurrFile = os.path.abspath (inspect.stack()[0][1])
print ("Executing File = %s\n" % strCurrFile)

# Initialize the DLL folder path to where the DLLs are located
strPathDllFolder = os.path.dirname (strCurrFile)
print ("Executing Dir  = %s\n" % strPathDllFolder)

# Add the DLL folder path to the system search path (before adding references)
sys.path.append (strPathDllFolder)

# Add a reference to each .NET assembly required
clr.AddReference ("DeviceIOLib")
clr.AddReference ("CmdLib8742")

# Import a class from a namespace
from Newport.DeviceIOLib import *
from NewFocus.PicomotorApp import CmdLib8742
from System.Text import StringBuilder

print ("Waiting for device discovery...")
# Call the class constructor to create an object
deviceIO = DeviceIOLib (True)
cmdLib8742 = CmdLib8742 (deviceIO)

# Set up USB to only discover picomotors (Controller model 8742)
deviceIO.SetUSBProductID (0x4000);

# Discover USB and Ethernet devices - delay 5 seconds
deviceIO.DiscoverDevices (5, 5000)

# Get the list of discovered devices
strDeviceKeys = np.array ([])
strDeviceKeys = deviceIO.GetDeviceKeys ()
nDeviceCount = deviceIO.GetDeviceCount ()
print ("Device Count = %d\n" % nDeviceCount)

# --- New Logic for Looping Command Input ---
picomotor_map = {} # Maps 'L' or 'R' to the actual device key (serial number)
open_device_keys = [] # List to track all successfully opened devices
strBldr = StringBuilder (64)
nReturn = -1

if (nDeviceCount > 0) :
    n = 0
    # First, open all devices and map their keys based on the serial number
    for oDeviceKey in strDeviceKeys :
        strDeviceKey = str (oDeviceKey)
        n = n + 1
        print (f"Device Key[{n}] = {strDeviceKey}")

        # If the device was opened
        if (deviceIO.Open (strDeviceKey)) :
            open_device_keys.append(strDeviceKey)
            
            # Identify the instrument to get the serial number
            strModel = ""
            strSerialNum = ""
            strFwVersion = ""
            strFwDate = ""
            
            # The IdentifyInstrument method is used to retrieve instrument details
            strModel, strSerialNum, strFwVersion, strFwDate = cmdLib8742.IdentifyInstrument (strDeviceKey, strModel, strSerialNum, strFwVersion, strFwDate)
            
            # Map the device key based on the serial number
            if (strSerialNum == "105969") :
                print (f"-> Mapped as 'L' (Serial: {strSerialNum})")
                picomotor_map['L'] = strDeviceKey
            elif (strSerialNum == "105970") :
                print (f"-> Mapped as 'R' (Serial: {strSerialNum})")
                picomotor_map['R'] = strDeviceKey
            else:
                print (f"-> Found device with serial {strSerialNum} but not mapped (not 105969 or 105970).")

            print (f"Model = {strModel}")
            print (f"Serial Num = {strSerialNum}")
            print (f"Fw Version = {strFwVersion}")
            print (f"Fw Date = {strFwDate}\n")

    # --- Start main loop to accept user commands ---
    if 'L' in picomotor_map or 'R' in picomotor_map:
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
                
                if target_key in picomotor_map:
                    device_key_to_use = picomotor_map[target_key]
                    
                    print(f"Sending command '{command}' to device '{target_key}' ({device_key_to_use})...")
                    
                    # Send the command using deviceIO.Query
                    strBldr.Remove (0, strBldr.Length)
                    # For a simple command (like a move command), deviceIO.Write may be used,
                    # but Query allows for command confirmation or error messages.
                    nReturn = deviceIO.Query (device_key_to_use, command, strBldr)
                    
                    print (f"Return Status = {nReturn}")
                    print (f"Response = {strBldr.ToString ()}\n")
                    
                else:
                    print(f"Error: Invalid target key '{target_key}'. Available keys: {', '.join(picomotor_map.keys())}.")
                    
            except EOFError:
                print("\nEOF received. Exiting loop...")
                break
            except Exception as e:
                print(f"An error occurred in the command loop: {e}")
                time.sleep(0.1) # Prevents fast looping on repeated errors
                
    else:
        print ("No target devices ('105969' or '105970') were discovered and mapped for control.\n")

    # --- Cleanup ---
    print("Shutting down and closing all open devices...")
    for key in open_device_keys:
        nReturn = deviceIO.Close (key)
        print(f"Closed device {key}. Status: {nReturn}")

else :
    print ("No devices discovered.\n")

# Shut down all communication
cmdLib8742.Shutdown ()
deviceIO.Shutdown ()
print ("Communication Shutdown complete.")