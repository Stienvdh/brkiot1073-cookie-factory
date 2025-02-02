import time, json, requests
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
        new_setting = check_router.check_packing2()
        state = get_json('state.json')
        if new_setting is False:
            loop_on.value = False
            state['packing2'] = False
        else:
            loop_on.value = True
            state['packing2'] = True
            state['cookies'] += 1
        write_json('state.json', state)
        time.sleep(5)

@app.route("/state")
def state():
    state = get_json('state.json')
    if state['packing2'] is True: 
        return 'ON'
    return 'OFF'

@app.route("/cookies")
def cookies():
    state = get_json('state.json')
    return str(state['cookies'])

@app.route("/")
def index():
    return render_template('index.html', component_name="packing machines", packing2_state=state())

if __name__ == "__main__":
   write_json('state.json', {
       'packing2': False,
       'cookies': 5
   })
   recording_on = Value('b', True)
   p = Process(target=plc_loop, args=(recording_on,))
   p.start()  
   app.run(host='0.0.0.0', port=8000, use_reloader=False)
   p.join()