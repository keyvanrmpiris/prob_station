# -*- coding: utf-8 -*-

import sys
import time
import os

# Add the parent directory to the path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ftd2xxhelper import Ftd2xxhelper


def main():
    WAVELENGTH = 1550
    POWER = 5
    INIT_WAVE = 1540
    END_WAVE =  1560
    SWEEP_RATE = 20
    # 1. Detect the one laser which is connected
    try:
        print("Searching for devices...")
        list_of_devices = Ftd2xxhelper.list_devices()

        if len(list_of_devices) < 1:
            print("No instruments found. Exiting.")
            sys.exit()
       
        # Select the first detected device automatically
        print("total devices found is:", len(list_of_devices))
        print(list_of_devices)
        device = list_of_devices[0]
        serial_number = device.SerialNumber.decode('utf-8')
        description = device.Description.decode('utf-8')
       
        print(f"Found Device: {description} (Serial: {serial_number})")
       
        # Connect to the instrument
        instrument = Ftd2xxhelper(serial_number.encode('utf-8'))
        print("Connection successful.\n")

    except Exception as e:
        print(f"Error connecting to device: {e}")
        sys.exit()

    try:
        # Helper function to write commands with a small delay
        def send_command(cmd, description):
            print(f"[{description}] Sending: {cmd}")
            instrument.write(cmd)
            time.sleep(0.5) # Wait for command to process

        # 2. Activate the laser (Turn LD ON)
        # [cite_start]Ref: TSL-570 Manual Page 71 (:POWer:STATE) [cite: 1760]
        send_command("POW:STAT 1", "Activating Laser")

        # 3. Set wavelength to a constant value (e.g., 1550nm)
        # [cite_start]Ref: TSL-570 Manual Page 67 (:WAVelength) [cite: 1696]
        send_command(f"WAV {WAVELENGTH}", "Setting Constant Wavelength to 1550nm")

        # 4. Set power to a constant value (e.g., 10 dBm)
        # [cite_start]Ref: TSL-570 Manual Page 72 (:POWer) [cite: 1770]
        send_command(f"POW {POWER}", "Setting Power to 10 dBm")

        # 5. Set sweep parameters
        # Set Start Wavelength (e.g., 1540nm)
        # [cite_start]Ref: TSL-570 Manual Page 75 (:WAVelength:SWEep:STARt) [cite: 1850]
        send_command(f"WAV:SWE:START {INIT_WAVE}", "Setting Sweep Start to 1540nm")

        # Set End Wavelength (e.g., 1560nm)
        # [cite_start]Ref: TSL-570 Manual Page 77 (:WAVelength:SWEep:STOP) [cite: 1857]
        send_command(f"WAV:SWE:STOP {END_WAVE}", "Setting Sweep Stop to 1560nm")

        # Set Sweep Rate (e.g., 20 nm/s)
        # [cite_start]Ref: TSL-570 Manual Page 81 (:WAVelength:SWEep:SPEed) [cite: 1932]
        send_command(f"WAV:SWE:SPE {SWEEP_RATE}", "Setting Sweep Rate to 20 nm/s")
 
        # 6. Start the sweep
        # [cite_start]Ref: TSL-570 Manual Page 86 (:WAVelength:SWEep) [cite: 1984]
        send_command("WAV:SWE 1", "Starting Sweep")

        # Wait loop to simulate operation (optional)
        print("Sweep is running... (Press Ctrl+C to abort early)")
        time.sleep(5)

        # 7. Pause the laser (Stop the sweep)
        # Sending 0 to WAV:SWE stops the sweep but keeps laser emission on (Pause/Stop Sweep)
        # [cite_start]Ref: TSL-570 Manual Page 86 [cite: 1984]
        send_command("WAV:SWE 0", "Pausing/Stopping Sweep")
       
        # If you want to completely disable the laser emission, uncomment the line below:
        # send_command("POW:STAT 0", "Disabling Laser Emission")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nClosing connection...")
        instrument.close_usb_connection()
        print("Done.")

if __name__ == '__main__':
    main()