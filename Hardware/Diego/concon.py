from time import sleep
from rpi_hardware_pwm import HardwarePWM
import os, serial

#from datetime import datetime
#read = datetime.now()
#write = datetime.now()
#print(read)

def loop(self):
    """Performs positioning and displays/exports the results."""
    position = Coordinates()
    status = self.pozyx.doPositioning(
        position, self.dimension, self.height, self.algorithm, remote_id=self.remote_id)
    if status == POZYX_SUCCESS:
        self.printPublishPosition(position)
    else:
        self.printPublishErrorCode("positioning")
if __name__ == '__main__':
    outPath = "pytoc"
    inPath = "ctopy"
    try:
        os.mkfifo(outPath, 0o600)
        print(f"Pipe named '{outPath}' is created successfully.\n")
    except:
        print(f"Pipe '{outPath}' already exists\n" )
    try:
        os.mkfifo(inPath, 0o600)
        print(f"Pipe named '{inPath}' is created successfully.\n")
    except:
        print(f"Pipe '{inPath}' already exists\n" )
    sleep(0.01)
    out = os.open(outPath, os.O_WRONLY)
    infile = os.open(inPath, os.O_RDONLY)
    servo = HardwarePWM(pwm_channel = 0, hz = 480)
    servoDuty= 75
    servo.start(servoDuty)
    
    motor = HardwarePWM(pwm_channel = 1, hz = 480)
    motorduty= 72
    motor.start(motorduty)
    userinput=5
    while True:
        #read = datetime.now()
        #loop()
        try:
            os.write(out, bytes(f"(0.0),(0.0),(0.0)\m","utf-8"))
            [motorduty, servoduty] = (float(x) for x in os.read(infile, 512).decode("utf-8").rstrip("\x00").split(","))
            servo.change_duty_cycle(servoduty)
            motor.change_duty_cycle(motorduty)
            print(f"({motorduty},{servoduty}")
        except:
            try:
                os.close(out)
                os.close(infile)
                os.unlink(outpath)
                os.unlink(inPath)
            except:
                print("dle\n")
            exit()
