import RPi.GPIO as GPIO
from time import sleep
from enum import Enum, auto
from flask import Flask, render_template, Response
import cv2
from cv import find_all_mushrooms, find_flowering_mushrooms, find_pink
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import dht11
import signal
import threading

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

growth_coverage = 0

camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640, 480))

state = State.INIT

GPIO.setmode(GPIO.BOARD)
sensor = dht11.DHT11(pin = 16)

idx = 0

app = Flask(__name__)

def handler(signum, frame):
    camera.close()
    exit(1)

def image_to_string(img):
    global idx
    global current_image
    new_image_path = image_path + str(idx) + '.png'
    cv2.imwrite(new_image_path, img)
    current_image = "./static/{}.png".format(idx)

def update_lcd_display():
    global lcd_display
    lcd_display = "humidity: {}%\nTemperature: {}F\nGrowth Coverage: {}%".format(humidity, temperature, growth_coverage)
    
def checker_thread():
    global idx
    while True:
        main()
        time.sleep(60)
        idx += 1
    
@app.route('/1')
def index():
    return render_template(
        'index.html',
        humidity=humidity,
        temperature=round(temperature, 1) ,
        growth_coverage=round(growth_coverage * 100, 4),
        current_image=current_image,
    )
    
def main():
    print('lets go')
    time.sleep(0.1)
    global state
    global growth_coverage
    global camera
    global rawCapture
    global idx
    global humidity
    global temperature
    if idx > 5:
        state = State.HARVEST
    if state == State.INIT:
        start_time = time.time()
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        image_to_string(image)
        sensor_result = sensor.read()
        humidity = sensor_result.humidity
        temperature = sensor_result.temperature * 1.8 + 32
        print('humidity: ', humidity, ', temperature: ', temperature)
        update_lcd_display()
        growth_coverage = find_pink(image)
        state = State.BUDDING
        rawCapture.truncate(0)

    elif state == State.BUDDING:
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        start_time = time.time()
        image_to_string(image)
        sensor_result = sensor.read()
        humidity = sensor_result.humidity
        temperature = sensor_result.temperature * 1.8 + 32
        print('humidity2: ', humidity, ', temperature: ', temperature)
        update_lcd_display()
        growth_coverage = find_pink(image)
        rawCapture.truncate(0)

        if find_flowering_mushrooms(image):
            state = State.HARVEST
        elif find_flowering_mushrooms(image):
            state = State.FLOWERING

    elif state == State.FLOWERING:
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        start_time = time.time()
        image_to_string(image)
        sensor_result = sensor.read()
        humidity = sensor_result.humidity
        temperature = sensor_result.temperature * 1.8 + 32
        print('humidity3: ', humidity, ', temperature: ', temperature)
        GPIO.cleanup()
        update_lcd_display()
        growth_coverage = find_pink(image)
        rawCapture.truncate(0)

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
        pass


if __name__ == '__main__':
    x = threading.Thread(target=checker_thread)
    x.start()
    app.run(host='100.70.10.68', threaded=True)
    print('main')
    signal.signal(signal.SIGINT, handler)
    main()
    camera.close()
    exit(1)
