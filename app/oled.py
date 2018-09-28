#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()

class Oled():

    def __init__(self):
        a = 1

    def draw_display_data(self, lat,lon,alt,timestamp,sats):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        # Write four lines of text.
        draw.text((x, top),       "Time: " + str(timestamp),  font=font, fill=255)
        draw.text((x, top+8),     "Sats: " + str(sats), font=font, fill=255)
        draw.text((x, top+16),    "LAT: " + str(lat),  font=font, fill=255)
        draw.text((x, top+24),    "LON: " + str(lon),  font=font, fill=255)
        draw.text((x, top+32),    "Alt: " + str(alt) + "m",  font=font, fill=255)
        self.display_image(image)
    
    def draw_splash_screen(self, image):
        image = Image.open(image).convert('1')
        self.display_image(image)
        time.sleep(2)

    def display_image(self, image):
        disp.image(image)
        disp.display()
        time.sleep(.1)
