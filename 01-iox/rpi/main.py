from flask import Flask
import smbus2
import time

app = Flask(__name__)
bus = smbus2.SMBus(1)
address = 0x38
rpi_address = '0.0.0.0'

def get_temperature():
    data = bus.read_i2c_block_data(address,0x71,1)
    if (data[0] | 0x08) == 0:
      return 24

    bus.write_i2c_block_data(address,0xac,[0x33,0x00])
    time.sleep(0.1)

    data = bus.read_i2c_block_data(address,0x71,7)

    Traw = ((data[3] & 0xf) << 16) + (data[4] << 8) + data[5]
    temperature = 200*float(Traw)/2**20 - 50

    return temperature

@app.route("/temperature")
def show_temperature():
    return str(get_temperature())

@app.route("/")
def hello_world():
    return f"""
    <meta http-equiv="refresh" content="2"> 
    <br><br><br>   
    <p><center><font size="300px">Temperature: {get_temperature()}</font></center></p>
    """

if __name__ == "__main__":
    app.run(host=rpi_address)