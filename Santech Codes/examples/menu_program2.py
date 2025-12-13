# -*- coding: utf-8 -*-

"""
Python LAN menu program for Santec TSL-570.
"""

import os
import sys
import time
import socket

LASER_IP = "192.168.0.100"
LASER_PORT = 5000   # <-- CORRECT PORT FOR TSL-570


# --- LAN Instrument Helper Class ---
class LanHelper:
    def __init__(self, ip, port):
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
class Santec:
    def __init__(self, instrument):
        self.instrument: LanHelper = instrument

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
            os.system('cls')
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


# Main menu
def main_menu():
    print("\nDetected LAN Instrument (TSL-570):")
    print(f"\n1. Device IP: {LASER_IP}, Port: {LASER_PORT}")

    while True:
        user_select = input("\nPress 1 to connect to the instrument: ")

        if user_select == "1":
            instrument = LanHelper(LASER_IP, LASER_PORT)
            reply = instrument.query_idn()
            print(f"\nCONNECTION SUCCESSFUL — Laser replied: {reply}")
            time.sleep(1)
            Santec(instrument).instrument_menu()
        else:
            print("\nInvalid selection... try again...")


if __name__ == '__main__':
    main_menu()
