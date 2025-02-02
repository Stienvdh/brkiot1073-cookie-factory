from flask import Flask, render_template
import requests
import json
import random

app = Flask(__name__)
temp_sensor_address = "<address-of-your-temperature-sensor>"

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def get_temperature():
    value = 18.0
    try:
        response = requests.get(f"http://{temp_sensor_address}:5000/temperature", verify=False).text
        value = float(response)
    except Exception as e:
        value = 30.0*random.random()
    temp_data = get_json('temperatures.json')
    current_temp = value
    new_temp_data = temp_data[1:] + [current_temp]
    write_json('temperatures.json', new_temp_data)
    return value

@app.route("/lasttemperature")
def read_last_temperature():
    temp_data = get_json('temperatures.json')
    current_temp = temp_data[-1]
    return str(current_temp)

@app.route("/temperature")
def show_temperature():
    return str(get_temperature())

@app.route("/")
def hello_world():
    temp_data = get_json('temperatures.json')
    current_temp = temp_data[-1]
    return render_template('index.html', component_name="temperature sensor", current_temperature=current_temp, temp_data=temp_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)