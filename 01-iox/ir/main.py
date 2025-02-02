from flask import Flask, render_template
import requests
import json
import random

app = Flask(__name__)
rpi_address = "<address-of-your-raspberry-pi>"

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def get_temperature():
    try:
        response = requests.get(f"http://{rpi_address}:5000/temperature", verify=False).text
        return int(response)
    except Exception as e:
        return 30.0*random.random()

@app.route("/temperature")
def show_temperature():
    return str(get_temperature())

@app.route("/")
def hello_world():
    temp_data = get_json('temperatures.json')
    oven_state = get_json('oven.json')
    current_temp = get_temperature()
    new_temp_data = temp_data[1:] + [current_temp]
    new_oven_state = oven_state
    if current_temp > 22:
        new_oven_state = False
    elif current_temp < 20:
        new_oven_state = True
    write_json('temperatures.json', new_temp_data)
    write_json('oven.json', {"state" : new_oven_state})
    oven_display = "OFF"
    if new_oven_state is True:
        oven_display = "ON"
    return render_template('index.html', current_temperature=current_temp, temp_data=new_temp_data, oven_state=oven_display)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)