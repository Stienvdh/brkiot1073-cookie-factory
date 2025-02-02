import time, json
from flask import Flask, render_template
from multiprocessing import Process, Value

app = Flask(__name__)

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def plc_loop(loop_on):
    while True:
        old_state = get_json('state.json')
        old_state['cookies'] += 1
        write_json('state.json', old_state)
        time.sleep(5)

@app.route("/ovenon")
def ovenon():
    state = get_json('state.json')
    return str(state['ovenison'])

@app.route("/ovenstate")
def ovenstate():
    state = get_json('state.json')
    if state['ovenison'] is False:
        return "OFF"
    return "ON"

@app.route("/cookies")
def cookies():
    state = get_json('state.json')
    return str(state['cookies'])

@app.route("/turnon")
def turnon():
    state = get_json('state.json')
    state['ovenison'] = True
    write_json('state.json', state)
    return state

@app.route("/turnoff")
def turnoff():
    state = get_json('state.json')
    state['ovenison'] = False
    write_json('state.json', state)
    return state

@app.route("/")
def index():
    state = get_json('state.json')
    oven_state = "ON"
    if state['ovenison'] is False:
        oven_state = "OFF"
    return render_template('index.html', component_name="oven", oven_state = oven_state, cookies = state['cookies'])

if __name__ == "__main__":
   write_json('state.json', {
       'cookies': 0,
       'ovenison': True
   })
   recording_on = Value('b', True)
   p = Process(target=plc_loop, args=(recording_on,))
   p.start()  
   app.run(host='0.0.0.0', port=8000, use_reloader=False)
   p.join()