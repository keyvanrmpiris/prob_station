# -*- coding: utf-8 -*-

"""
Python LAN menu program for Santec TSL-570.
"""

import os
import sys
import time
import socket
from .ftd2xxhelper import Ftd2xxhelper


# LASER_IP = "192.168.0.100"
# LASER_PORT = 5000   # <-- CORRECT PORT FOR TSL-570

# --- LAN Instrument Helper Class ---
class LanHelper:
    def __init__(self):
        self.ip = ip
        self.port = port

    def send(self, cmd):
        try:
            with socket.create_connection((self.ip, self.port), timeout=5) as s:

                # TSL-570 REQUIRES CRLF TERMINATION
                msg = (cmd + "\r\n").encode("ascii")
                s.sendall(msg)

                s.settimeout(3)
                data = s.recv(4096)
                return data.decode(errors="ignore").strip()

        except Exception as e:
            return f"ERROR: {e}"

    def query(self, cmd):
        return self.send(cmd)

    def write(self, cmd):
        return self.send(cmd)

    def query_idn(self):
        return self.send("IDN?")


# Instrument control class
class Laser:
    def __init__(self):
        self.list_devices = []
        self.instrument = None
        

    def connect(self):
        # 1. Detect the one laser which is connected
        try:
            print("Searching for devices...")
            list_of_devices = Ftd2xxhelper.list_devices()

            if len(list_of_devices) < 1:
                print("No instruments found. Exiting.")
                sys.exit()
        
            # Select the first detected device automatically
            device = list_of_devices[0]
            serial_number = device.SerialNumber.decode('utf-8')
            description = device.Description.decode('utf-8')
        
            print(f"Found Device: {description} (Serial: {serial_number})")
        
            # Connect to the instrument
            self.instrument = Ftd2xxhelper(serial_number.encode('utf-8'))
            print("Connection successful.\n")

        except Exception as e:
            print(f"Error connecting to device: {e}")
            sys.exit()

    def query_instrument(self):
        command = input("\nEnter the command to Query (eg. POW ?) ").strip()
        reply = self.instrument.query(command)
        print(reply)
        input("\nPress any key to continue...")
        return True

    def write_instrument(self):
        command = input("\nEnter the command to Write (eg. POW 1) ").strip()
        reply = self.instrument.write(command)
        print("\nCommand written:", reply)
        time.sleep(0.5)
        return True

    def query_idn_instrument(self):
        reply = self.instrument.query_idn()
        print(reply)
        input("\nPress any key to continue...")
        return True

    def close_connection(self):
        print("\nClosing LAN connection...")
        time.sleep(0.2)

    def goto_main_menu(self):
        self.close_connection()
        main_menu()

    def exit_program(self):
        self.close_connection()
        sys.exit()

    def instrument_menu(self):
        menu = {
            '1': self.query_instrument,
            '2': self.write_instrument,
            '3': self.query_idn_instrument,
            '4': self.goto_main_menu,
            '5': self.exit_program
        }

        while True:
            user_operation = input(
                "\nInstrument Menu:-"
                "\n1. Query Instrument"
                "\n2. Write Instrument"
                "\n3. Query IDN Instrument"
                "\n4. Go to Main Menu"
                "\n5. Exit"
                "\nSelect an operation: "
            )

            if user_operation in menu:
                menu[user_operation]()
            else:
                print("\nInvalid selection... try again...")
                time.sleep(1)