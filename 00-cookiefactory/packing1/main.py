import time, json
from flask import Flask, render_template
from multiprocessing import Process, Value
import check_router

app = Flask(__name__)

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def plc_loop(loop_on):
    while True:
        new_packing_setting = check_router.check_packing1()
        old_state = get_json('state.json')
        if new_packing_setting is True:
            loop_on.value = True
            old_state['packing1'] = True
            old_state['cookies'] += 1
        else:
            loop_on.value = False
            old_state['packing1'] = False
        write_json('state.json', old_state)
        time.sleep(5)

@app.route("/cookies")
def cookies():
    state = get_json('state.json')
    return str(state['cookies'])

@app.route("/state")
def state():
    state = get_json('state.json')
    if state['packing1'] is True: 
        return 'ON'
    return 'OFF'

@app.route("/pack1on")
def pack1on():
    state = get_json('state.json')
    if state['packing1'] is True: 
        return str(True)
    return str(False)

@app.route("/")
def index():
    return render_template('index.html', component_name="packing machines", packing1_state=state())

if __name__ == "__main__":
   write_json('state.json', {
       'packing1': True,
       'cookies' : 0
   })
   recording_on = Value('b', True)
   p = Process(target=plc_loop, args=(recording_on,))
   p.start()  
   app.run(host='0.0.0.0', port=8000, use_reloader=False)
   p.join()