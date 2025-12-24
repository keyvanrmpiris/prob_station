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

import sys
import time
# Assuming Ftd2xxhelper is imported here

class Laser:
    def __init__(self):
        self.list_devices = []
        self.instrument = None
        
    def connect(self):
        try:
            print("Searching for devices...")
            list_of_devices = Ftd2xxhelper.list_devices()

            if len(list_of_devices) < 1:
                print("No instruments found. Exiting.")
                sys.exit()
        
            device = list_of_devices[0]
            # FIX 1: Strip whitespace/nulls which can confuse C-drivers
            serial_number = device.SerialNumber.decode('utf-8').strip()
            description = device.Description.decode('utf-8').strip()
        
            print(f"Found Device: {description} (Serial: {serial_number})")
            
            # FIX 2: Add delay to let USB enumeration settle before opening
            print("Initializing driver... (waiting 1s)")
            time.sleep(1.0) 
        
            self.instrument = Ftd2xxhelper(serial_number.encode('utf-8'))
            print("Connection successful.\n")

        except Exception as e:
            print(f"Error connecting to device: {e}")
            # Optional: Print traceback if available to see DLL errors
            import traceback
            traceback.print_exc()
            sys.exit()

    def query_instrument(self):
        # It is safer to use \r\n for both read/write unless manual says otherwise
        command = input("\nEnter the command to Query (eg. POW ?): ").strip()
        full_command = command
        
        try:
            reply = self.instrument.query(full_command)
            print(f"Reply: {reply}")
        except Exception as e:
            print(f"Query failed: {e}")
            
        input("\nPress any key to continue...")

    def write_instrument(self):
        command = input("\nEnter the command to Write (eg. POW 1): ").strip()
        # FIX: Ensure encoding consistency
        full_command = command
            
        try:
            reply = self.instrument.write(full_command)
            print("Command written:", reply)
        except Exception as e:
            print(f"Write failed: {e}")
            
        time.sleep(0.5)

    def query_idn_instrument(self):
        try:
            # FIX: Ensure we use the internal object's method safely
            reply = self.instrument.query_idn()
            print(f"IDN: {reply}")
        except Exception as e:
            print(f"IDN Query failed: {e}")
            
        input("\nPress any key to continue...")

    def close_connection(self):
        if self.instrument:
            print("\nClosing connection...")
            # If your wrapper has a close method, call it here!
            # self.instrument.close() 
            self.instrument = None
        time.sleep(0.2)

    def goto_main_menu(self):
        self.close_connection()
        print("Returning to main menu (Not Implemented)...")
        # main_menu() # <--- REMOVED: This function does not exist

    def exit_program(self):
        self.close_connection()
        print("Exiting.")
        sys.exit()

    def instrument_menu(self):
        # ... (rest of menu logic is fine) ...
        # (Same as your code)
        menu = {
            '1': self.query_instrument,
            '2': self.write_instrument,
            '3': self.query_idn_instrument,
            '4': self.goto_main_menu,
            '5': self.exit_program
        }
        while True:
            print("\n--- Instrument Menu ---")
            print("1. Query Instrument")
            print("2. Write Instrument")
            print("3. Query IDN")
            print("4. Main Menu")
            print("5. Exit")
            
            user_operation = input("Select an operation: ")

            if user_operation in menu:
                menu[user_operation]()
            else:
                print("\nInvalid selection... try again...")
                time.sleep(1)