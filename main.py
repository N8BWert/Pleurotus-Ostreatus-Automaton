from enum import Enum, auto
from flask import Flask, render_template
import cv2

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
    current_image = format("<img src='{}' class='mushroom_image' height='10px' width='10px'>", new_image_path)

def update_lcd_display():
    lcd_display = format("humidity: {}%\nTemperature: {}C\nLight Intensity: {}cd", humidity, temperature, light_intensity)

def main():
    state = state.INIT
    while (True):
        if state == state.INIT:
            pass

        elif state == state.BUDDING:
            pass

        elif state == state.FLOWERING:
            pass

        elif state == state.HARVEST:
            pass
    update_lcd_display()



if __name__ == '__main__':
    app.run(debug=True, host='127.17.0.1')
    main()