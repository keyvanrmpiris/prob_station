import yaml
import time
import threading
import msvcrt # Standard Windows library for key detection

from drivers.laser_driver import Laser
from drivers.connexcc_driver import Conexcc
from drivers.rigol_driver import Rigol
from drivers.pcm_driver import Pcm
def main():
    with open('config/instruments.yaml', 'r') as f:
        config = yaml.safe_load(f)

    ######Laser######
    

    # laser = Laser()
    # laser.connect()
    # reply= laser.instrument.query_idn()
    # print(f"\nCONNECTION SUCCESSFUL — Laser replied: {reply}")
    # laser.instrument_menu()

    ######pcm########
    # pcm = Pcm()
    # pcm.connect()
    # pcm.send_command("")


    # ####conexcc######
    # conex = Conexcc()
    # conex.connect()
    # device_id = conex.send_command("ID?",0)
    # print(device_id)
    # print("Starting homing sequence (Origin Search)... This may take time.")
    # conex.send_command("OR",0)
    # while True:
    #     status = conex.send_command("TS", 0)
    #     # The response looks like '1TS000032' - we check the last two digits
    #     state = status[-2:] 
    #     if state in ['32', '33', '34']: # Ready states
    #         print("Homing complete.")
    #         break
    #     time.sleep(0.5)
    # a=10
    # conex.send_command(f"PA{a}",0)
    # while True:
    #     status = conex.send_command("TS", 0)
    #     # The response looks like '1TS000032' - we check the last two digits
    #     state = status[-2:] 
    #     if state in ['32', '33', '34']: # Ready states
    #         print("moving complete.")
    #         break
    #     time.sleep(0.5)
    # current_pos = conex.send_command("TP",0)
    # print(f"Current position: {current_pos} mm")




    # #####Rigol########
    # rgl = Rigol()
    # rgl.connect()
    # rgl.set_vertical_scale()
    # rgl.get_vertical_params()
    # rgl.get_trigger_source()
    # rgl.monitor_measurements()
    # rgl.disconnect()
    # return

    # laser = Laser()
    # rgl = Rigol()
    
    # laser.connect()
    # reply= laser.instrument.query_idn()
    # print(f"\nCONNECTION SUCCESSFUL — Laser replied: {reply}")
    # laser.instrument.write("POW:STAT 1")
    # laser.instrument.write("POW 10")
    # # laser.instrument_menu()
    # input("\nEnter the a key ")
    # print("state1")

    
    # rgl.connect()
    # rgl.set_vertical_scale()
    # rgl.get_vertical_params()
    # rgl.get_trigger_source()
    # rgl.monitor_measurements()

    # input("\nEnter the a key 2")
    # print("state2")
    # rgl.disconnect()
    # laser.instrument.close_connection()

    # --- Setup ---
    laser = Laser()
    rgl = Rigol()
    pcm = Pcm()
    conex = Conexcc()

    laser.connect()
    pcm.connect()
    conex.connect()
    rgl.connect()

    # Start the silent background thread
    rgl.monitor_measurements()

    print("\n" + "="*40)
    print("  SYSTEM READY")
    print("  Press ENTER to pause monitoring and type a command.")
    print("="*40)

    try:
        while True:
            # --- MODE 1: MONITORING ---
            # Loop here until the user hits a key
            print("\n") # formatting spacer
            while not msvcrt.kbhit():
                # Print the Rigol status over and over on the same line
                # The 50 spaces ensure we wipe out old text
                print(f"\r{rgl.get_status()} {' '*20}", end='', flush=True)
                time.sleep(0.1)

            # --- MODE 2: COMMAND ENTRY ---
            # If we get here, a key was pressed!
            # Clear the keyboard buffer (consume the keypress)
            msvcrt.getch() 
            
            # Now we can use normal input() because we stopped the printing loop above
            print("\n\n--- PAUSED: Enter Command (l/c/p/q) ---")
            raw = input(">> ").strip().split(maxsplit=1)

            if not raw: continue # If they just hit enter, go back to monitoring

            action = raw[0].lower()
            arg = raw[1] if len(raw) > 1 else ""

            if action == 'l':
                laser.instrument.write(f"{arg}")
                print(f"Laser send command {arg} to the laser")
            
            elif action == 'c':
                conex.send_command(f"PA{arg}", 0)
                print(f"Conex moving to {arg}")

            elif action == 'p':
                pcm.send_command(arg)

            elif action == 'q':
                break
            
            input("press enter to continue)")
            print("Resuming monitoring...", end='')
            time.sleep(1) # Give user a second to read the confirmation

    finally:
        rgl.stop_monitoring()
        rgl.disconnect()
        laser.instrument.close_connection()
        pcm.close_connection()

if __name__=="__main__":
    main()