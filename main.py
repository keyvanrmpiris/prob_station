import yaml
from drivers.laser_driver import Laser
from drivers.connexcc_driver import Conexcc
from drivers.rigol_driver import Rigol
from drivers.pcm_driver import Pcm
def main():
    with open('config/instruments.yaml', 'r') as f:
        config = yaml.safe_load(f)

    ######Laser######
    print (config["sentec_laser"]["port"])

    laser = Laser(config["sentec_laser"]["ip"],config["sentec_laser"]["port"])
    laser.instrument.query_idn()
    laser.instrument_menu()

    ######pcm########
    pcm = Pcm()
    pcm.connect()
    pcm.send_command()


    ####conexcc######
    conex = Conexcc()
    conex.connect()
    device_id = conex.send_command("ID?",0)



    #####Rigol########
    rgl = Rigole()
    rgl.connect()
    rgl.send_command()

    return


if __name__=="__main__":
    main()