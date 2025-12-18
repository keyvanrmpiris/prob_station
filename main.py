import yaml
import time
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
    pcm = Pcm()
    pcm.connect()
    pcm.send_command()


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


if __name__=="__main__":
    main()