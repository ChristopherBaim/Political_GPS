import PoliticalGPS as PGPS
import time
from gps3 import gps3
import json
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import pigpio


# For use with LED or LCD backlight. Have to start pigpio daemon before using
pi = pigpio.pi()

if not pi.connected:
    print("exit")
    exit()

def setColor(Red, Green, Blue):
    pi.set_PWM_dutycycle(5,Red)#RED
    pi.set_PWM_dutycycle(6,Green) #GREEN
    pi.set_PWM_dutycycle(13,Blue) #BLUE

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config (CHRIS'S PINOUT):
lcd_rs = digitalio.DigitalInOut(board.D17)
lcd_en = digitalio.DigitalInOut(board.D27)
lcd_d7 = digitalio.DigitalInOut(board.D25)
lcd_d6 = digitalio.DigitalInOut(board.D24)
lcd_d5 = digitalio.DigitalInOut(board.D23)
lcd_d4 = digitalio.DigitalInOut(board.D22)
lcd_backlight = digitalio.DigitalInOut(board.D26)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.backlight = False

setColor(150,255,255)
lcd.message = "Loading Data"
lcd.blink= True

NonRingShapes = []
RingShapes = []

startTime = time.time()

PGPS.readData(NonRingShapes, '/home/pi/Desktop/Merged Attributes Nodes Test/Non-Rings.csv')
PGPS.readData(RingShapes, '/home/pi/Desktop/Merged Attributes Nodes Test/Rings.csv')

endTime = time.time()
totalTime = str(endTime-startTime)
print(endTime-startTime)

setColor(0,0,0)
time.sleep(1)
setColor(150,255,255)

lcd.message = "Data Loaded: " + totalTime
lcd.blink= True
time.sleep(3)

lcd.message = "Acquiring\nSatellites"
lcd.blink= True

#TestX = float(input('Lat: '))
#TestY = float(input('Long: '))

#Lat = 44.1596
#Lon = -79.3945

curLat = 0
curLon = 0
dataClass = "Null"

gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

curWinner = "none"
while(True):
    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)
            print(new_data)
            try:
                data = json.loads(new_data)
                #print(data)
                dataClass = data['class']
            
                #print(dataClass)
            except:
                print("ERROR: Missing start char")
            if dataClass == "TPV":
                try:
                    curLon = float(data_stream.TPV['lon'])
                    curLat = float(data_stream.TPV['lat'])

                    PGPS.calcDistance(curLat, curLon, NonRingShapes)
                    PGPS.calcDistance(curLat, curLon, RingShapes)

                    NonRingShapes = sorted(NonRingShapes, key=lambda Shapes: Shapes.Distance)
                    RingShapes = sorted(RingShapes, key=lambda Shapes: Shapes.Distance)

                    Name, Winner = PGPS.findRiding(NonRingShapes, RingShapes, curLat, curLon)
                    print(Name)
                    print(Winner)
                    if Winner != curWinner:
                        curWinner = Winner
                        lcd.clear()
                        lcd.blink = False
                        lcd.message = Name + "\n" + Winner
                        
                        if Winner == "Liberal":
                            setColor(255,0,0)
                        elif Winner == "Bloc Quebecois":
                            setColor(0,200,200)
                        elif Winner == "Conservative":
                            setColor(0,0,255)
                        elif Winner == "NDP-New Democratic Party":
                            setColor(200,50,0)
                        elif Winner == "Green Party":
                            setColor(0,255,0)
                except:
                    print("ERROR: No data")
                    #make this into blinking LED (finding satellites)
            else:
                print("wrong data type")

            #time.sleep(5)

                        
