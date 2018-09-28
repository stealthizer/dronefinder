import serial
import time
import multiprocessing
import pynmea2
from oled import Oled

## Change this to match your local settings
SERIAL_PORT = '/dev/ttyS0'
SERIAL_BAUDRATE = 9600

oled = Oled()

oled.draw_splash_screen('/app/drone.jpg')

class SerialProcess(multiprocessing.Process):

    def __init__(self, input_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

    def convert_latitude(self, GGA):
        if GGA.lat is not '':
            DD = int(float(GGA.lat)/100)
            SS = float(GGA.lat) - DD * 100
            LatDec = DD + SS/60
            if GGA.lat_dir is 'S':
                LatDec = LatDec * -1
            return round(LatDec,6)
        else:
            return 0

    def convert_longitude(self, GGA):
        if GGA.lon is not '':
            DD = int(float(GGA.lon)/100)
            SS = float(GGA.lon) - DD * 100
            LonDec = DD + SS/60
            if GGA.lon_dir is 'W':
                LonDec = LonDec * -1
            return round(LonDec,6)
        else:
            return 0

    def create_map_uri(self, lat,lon,label):
        return "https://www.google.com/maps/place/" + lat + "," + lon

    def close(self):
        self.sp.close()

    def writeSerial(self, data):
        self.sp.write(data.encode('utf-8'))
        # time.sleep(1)

    def readSerial(self):
        serialdata = self.sp.readline().decode('utf-8').replace("\n", "")
        return serialdata

    def run(self):
        self.sp.flushInput()

        while True:
            # look for incoming tornado request
            if not self.input_queue.empty():
                data = self.input_queue.get()
                # send it to the serial device
                self.writeSerial(data)
                print("writing to serial: " + data)

            # look for incoming serial data
            if (self.sp.inWaiting() > 0):
                data = self.readSerial()
                if data.find('GGA') >0:
                  try:
                    msg = pynmea2.parse(data)
                  except:
                    continue
                  else:
                    display = ""
                    timestamp = msg.timestamp
                    print("Time: %s" % timestamp)
                    display = display + "Timestamp: " + str(timestamp) + "<br>"
                    num_sats = msg.num_sats
                    print("Satelites: %s" % (num_sats))
                    display = display + "Sats: " + str(num_sats) + "<br>"
                    altitude = str(msg.altitude)
                    display = display + "Altitude: " + altitude + "m" + "<br>"
                    print("Altitude: " + altitude + "m")
                    latitude = self.convert_latitude(msg)
                    print(latitude)
                    display = display + "Longitude: " + str(latitude) + "<br>"
                    longitude = self.convert_longitude(msg)
                    print(longitude)
                    display = display + "Latitude: " + str(longitude) + "<br>"
                    display = display + "<a href=" + str(self.create_map_uri(str(latitude), str(longitude), "Lost Drone")) + ">Show Drone in Google Maps</a><br>"
                    oled.draw_display_data(latitude, longitude, altitude, timestamp, num_sats)
                    print("reading from serial: " + data)
                    # send it back to tornado
                    self.output_queue.put(display)
