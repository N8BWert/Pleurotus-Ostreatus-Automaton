import RPi.GPIO as GPIO
from time import sleep
from enum import Enum, auto
from flask import Flask, render_template
import cv2
from cv import find_all_mushrooms, find_flowering_mushrooms
import time
#from picamera.array import piRGBArray
#from picamera import PiCamera

class state(Enum):
    INIT = auto()
    BUDDING = auto()
    FLOWERING = auto()
    HARVEST = auto()


app = Flask(__name__)

humidity = 65
temperature = 10
light_intensity = 5
current_image = "./static/mushroom_1.png"

image_path = './static/'
current_timestep = 0

lcd_display = ""

start_time = 0

#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 1/60
#rawCapture = PiRGBArray(camera)

@app.route('/1')
def index():
    return render_template(
        'index.html',
        humidity=humidity,
        temperature=temperature,
        light_intensity=light_intensity,
        current_image=current_image
    )

def image_to_string(img):
    new_image_path = image_path + str(current_timestep) + '.png'
    cv2.imwrite(new_image_path, img)
    current_image = new_image_path

def update_lcd_display():
    lcd_display = format("humidity: {}%\nTemperature: {}C\nLight Intensity: {}cd", humidity, temperature, light_intensity)

def main():
    time.sleep(0.1)
    state = state.INIT
    while (True):
        if state == state.INIT:
            start_time = time.time()
            cv2.im

        elif state == state.BUDDING:
            pass

        elif state == state.FLOWERING:
            pass

        elif state == state.HARVEST:
            pass

        if (time.time() - start_time > 60):
            #camera.capture(rawCapture, format="bgr")
            #image = rawCapture.array
            start_time = time.time()
            pass

        #if find_all_mushrooms(image):
            #state = State.FLOWERING
        #elif find_flowering_mushrooms(image):
            #state = State.HARVEST
        #image_to_string(image)
        update_lcd_display()
        GPIO.setmode(GPIO.BOARD)

        ControlPin = [7, 11, 13, 15]

        for pin in ControlPin:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        seq = [ [1,0,0,0],
                [1,1,0,0],
                [0,1,0,0],
                [0,1,1,0],
                [0,1,1,0],
                [0,0,1,0],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1] ]

        for i in range(512):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(ControlPin[pin], seq[halfstep][pin])
                sleep(0.001)

        GPIO.cleanup()


if __name__ == '__main__':
    app.run(debug=True, host='127.17.0.1')
    main()