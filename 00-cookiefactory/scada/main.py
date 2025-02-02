from flask import Flask, render_template
import json, requests

app = Flask(__name__)

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

@app.route("/")
def hello_world():
    temperature = requests.get('http://temperature:8000/lasttemperature', verify=False).text
    oven = requests.get('http://oven:8000/ovenstate', verify=False).text
    packing1 = requests.get('http://packing1:8000/state', verify=False).text
    oven_cookies = requests.get('http://oven:8000/cookies', verify=False).text
    p1cookies = requests.get('http://packing1:8000/cookies', verify=False).text
    p2cookies = requests.get('http://packing2:8000/cookies', verify=False).text
    return render_template('index.html', component_name="SCADA", temperature=temperature, oven_state = oven, packing1=packing1, cookies = oven_cookies, cookiesp1 = p1cookies, cookiesp2 = p2cookies)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)