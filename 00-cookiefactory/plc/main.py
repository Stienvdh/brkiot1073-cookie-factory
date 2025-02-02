import time, json, requests
from flask import Flask, render_template
from multiprocessing import Process, Value

app = Flask(__name__)

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def check_temperature():
    MAX_TEMP = 23.0
    MIN_TEMP = 17.0
    temperature = float(requests.get('http://temperature:8000/temperature', verify=False).text)
    state = bool(requests.get('http://oven:8000/ovenon', verify=False).text)
    app.logger.info(f"Temperature {temperature} state {state}")
    if temperature > MAX_TEMP:
        return False
    elif temperature < MIN_TEMP:
        return True
    return None

def get_temperature():
    return float(requests.get('http://temperature:8000/lasttemperature', verify=False).text)

def plc_loop(loop_on):
    while True:
        new_oven_setting = check_temperature()
        state = get_json('state.json')
        if new_oven_setting is True:
            loop_on.value = True
            state['shouldovenbeon'] = True
            requests.get('http://oven:8000/turnon', verify=False)
        elif new_oven_setting is False:
            loop_on.value = False
            state['shouldovenbeon'] = False
            requests.get('http://oven:8000/turnoff', verify=False)
        state['lasttemperature'] = get_temperature()
        write_json('state.json', state)
        time.sleep(5)
    
@app.route("/")
def index():
    state = get_json('state.json')
    oven_state = "ON"
    if state['shouldovenbeon'] is False:
        oven_state = "OFF"
    return render_template('index.html', component_name="oven", temperature = state['lasttemperature'], oven_state = oven_state)

if __name__ == "__main__":
   write_json('state.json', {
       'shouldovenbeon': True,
       'lasttemperature': 19.0
   })
   recording_on = Value('b', True)
   p = Process(target=plc_loop, args=(recording_on,))
   p.start()  
   app.run(host='0.0.0.0', port=8000, use_reloader=False)
   p.join()