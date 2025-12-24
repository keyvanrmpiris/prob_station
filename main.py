import yaml
import time
import threading
import msvcrt # Standard Windows library for key detection

from drivers.laser_driver import Laser
from drivers.connexcc_driver import Conexcc
from drivers.rigol_driver import Rigol
from drivers.pcm_driver import Pcm
def main():
    

    # laser = Laser()
    # laser.connect()
    # reply= laser.instrument.query_idn()
    # print(f"\nCONNECTION SUCCESSFUL — Laser replied: {reply}")
    # laser.instrument_menu()
    # input ("waiting for the laser")


    # try:
    #     print("1. Instantiating Laser...")
    #     laser = Laser()
        
    #     print("2. Connecting to Laser...")
    #     laser.connect()
        
    #     print("3. Querying IDN (Sending command)...")
    #     # This is the most likely crash point based on your logs
    #     reply = laser.instrument.query_idn() 
        
    #     print(f"4. IDN Received: {reply}")
    #     print(f"\nCONNECTION SUCCESSFUL — Laser replied: {reply}")
        
    #     print("5. Opening Menu...")
    #     laser.instrument_menu()
        
    #     print("6. Waiting for input...")
    #     input("waiting for the laser")
        
    # except Exception as e:
    #     print("\n!!!!!!!! ERROR CAUGHT !!!!!!!!")
    #     print(f"Error Type: {type(e).__name__}")
    #     print(f"Error Message: {e}")
    #     traceback.print_exc()
        

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

    # # Initialize
    # rgl = Rigol()
    # laser = Laser()
    # conex = Conexcc()
    # pcm = Pcm()

    # # Connections
    # rgl.connect()
    # laser.connect()
    # pcm.connect()
    # conex.connect()

    # 1. Initialize all drivers
    laser = Laser()
    rgl = Rigol()
    pcm = Pcm()
    conex = Conexcc() # Assuming you use this for other motors

    # 2. Connect Hardware
    laser.connect()
    pcm.connect()
    conex.connect()
    rgl.connect()

    # 3. Start Rigol Background Monitoring (Non-blocking)
    rgl.monitor_measurements() 

    print("\n" + "="*30)
    print("  SYSTEM READY - CONTINUOUS MONITORING ACTIVE")
    print("="*30)
    print("Commands:")
    print("  l [val]  -> Set Laser Power")
    print("  c [pos]  -> Move Conex Motor")
    print("  p [cmd]  -> PCM Command (e.g., 'p L3PR1000')")
    print("  q        -> Quit")

    try:
        while True:
            # We use a space-split to separate command type from value
            # Example: "l 10" or "p RREL500"
            raw = input("\n>> ").strip().split(maxsplit=1)
            if not raw: continue
            
            action = raw[0].lower()
            arg = raw[1] if len(raw) > 1 else ""

            if action == 'l':
                laser.instrument.write(f"{arg}")
                print(f"Laser power set to {arg}")

            elif action == 'c':
                conex.send_command(f"{arg}", 0)
                print(f"Conex moving to {arg}")

            elif action == 'p':
                # Pass the command directly to our new PCM method
                pcm.send_command(arg)

            elif action == 'q':
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("\nShutting down...")
        rgl.stop_monitoring()
        # pcm.close_connection()
        laser.instrument.close_connection()
        rgl.disconnect()

if __name__=="__main__":
    main()