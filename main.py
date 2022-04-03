import RPi.GPIO as GPIO
from time import sleep
from enum import Enum, auto
from flask import Flask, render_template, Response
import cv2
from cv import find_all_mushrooms, find_flowering_mushrooms
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import signal

class State(Enum):
    INIT = auto()
    BUDDING = auto()
    FLOWERING = auto()
    HARVEST = auto()
    FINALIZING = auto()


humidity = 65
temperature = 10
light_intensity = 5
current_image = "./static/mushroom_1.png"

image_path = './static/'
current_timestep = 0

lcd_display = ""

start_time = 0

time_left_before_harvest = 60

print('precamera')

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

app = Flask(__name__)

def handler(signum, frame):
    camera.close()
    exit(1)

def image_to_string(img):
    new_image_path = image_path + str(current_timestep) + '.png'
    cv2.imwrite(new_image_path, img)
    current_timestep += 1
    return new_image_path

def update_lcd_display():
    lcd_display = "humidity: {}%\nTemperature: {}C\nLight Intensity: {}cd".format(humidity, temperature, light_intensity)

def main():
    time_left_before_harvest -= (time.time() - start_time)
    start_time = time.time()
    time.sleep(0.1)
    state = State.INIT
    global current_image
    while (True):
        if state == State.INIT:
            start_time = time.time()
            camera.capture(rawCapture, format="bgr")
            image = rawCapture.array
            current_image = image_to_string(image)
            update_lcd_display()
            state = State.BUDDING

        elif state == State.BUDDING:
            if (time.time() - start_time > 60):
                camera.capture(rawCapture, format="bgr")
                image = rawCapture.array
                start_time = time.time()
                current_image = image_to_string(image)
                update_lcd_display()

                if find_flowering_mushrooms(image):
                    state = State.HARVEST
                elif find_flowering_mushrooms(image):
                    state = State.FLOWERING

        elif state == State.FLOWERING:
            if (time.time() - start_time > 60):
                camera.capture(rawCapture, format="bgr")
                image = rawCapture.array
                start_time = time.time()
                current_image = image_to_string(image)
                update_lcd_display()

                if find_flowering_mushrooms(image):
                    state = State.HARVEST

        elif state == State.HARVEST:
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

            state = State.FINALIZING

        elif state == State.FINALIZING:
            break

    if time_left_before_harvest < 0:
        state = State.HARVEST
        time_left_before_harvest = 10000


if __name__ == '__main__':
    app.run(host='100.70.10.68', threaded=True)
    print('main')
    signal.signal(signal.SIGINT, handler)
    main()
    camera.close()
    exit(1)

@app.route('/1')
def index():
    return render_template(
        'index.html',
        humidity=humidity,
        temperature=temperature,
        light_intensity=light_intensity,
        current_image=current_image
    )