import display
import mch22
import buttons
import machine
from neopixel import NeoPixel

IMG_BASE="/apps/python/meme/assets/nyan-{}.png"
IMG_NUM=12
IMG_SUB="Hanfi (de/en)"

#RAINBOW = [(148,0,211),(75,0,130),(0,0,255),(0,255,0),(255,255,0),(255,127,0),(255,0,0)]
RAINBOW = [(74,0,106),(39,0,65),(0,0,127),(0,127,0),(127,127,0),(127,63,0),(127,0,0)]

image_cache = [None]*IMG_NUM

pixel_cache = NeoPixel(machine.Pin(5,machine.Pin.OUT),5)
pixel_power = machine.Pin(19,machine.Pin.OUT)


def displayInfo():
    display.drawFill(0xFFFFFF)
    dim = display.size()
    display.drawText(0,0, "Hello World", 0x000000, "PermanentMarker22")
    display.drawText(0,25, "W:{} H: {}".format(dim[0],dim[1]),0x000000, "PermanentMarker22")
    display.flush()
    machine.lightsleep(2000)

def displayNext(i):
    if not image_cache[i]:
        with open(IMG_BASE.format(i), 'rb',) as f:
            image_cache[i] = f.read()
    display.drawFill(0xFFFFFF)
    display.drawPng(0,0,image_cache[i])
    display.drawText(100,200,IMG_SUB, 0xFFFFFF, "PermanentMarker22")
    display.flush()

def displayRainbow(j):
    for i in range(5):
        pixel_cache[i] = RAINBOW[(i+j)%len(RAINBOW)]
    pixel_cache.write()
    
def displayAnimated():
    i = 0
    j = 0
    while True:
        displayNext(i)
        i = (i+1)%len(image_cache)
        displayRainbow(j)
        j = (j+1)%len(RAINBOW)
        machine.lightsleep(100)
        #time.sleep(0.2)

def enablePixels(pressed):
    if pressed:
        if pixel_power.value():
            pixel_power.off()
        else:
            pixel_power.on()

def buttonExitApp(pressed):
    mch22.exit_python()

buttons.attach(buttons.BTN_HOME, buttonExitApp)
buttons.attach(buttons.BTN_B, buttonExitApp)
buttons.attach(buttons.BTN_A, enablePixels)



#displayInfo()
displayAnimated()
