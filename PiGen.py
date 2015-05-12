from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, flash, render_template, request, redirect
from flask import Markup
import math
from lib2to3.fixer_util import String
import struct
import RPi.GPIO as GPIO


ip = '192.168.0.99'

# setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO pins
W_CLK = 15
FQ_UD = 16
DATA = 18
RESET = 22
Pon = 7

# setup IO bits
GPIO.setup(W_CLK, GPIO.OUT)
GPIO.setup(FQ_UD, GPIO.OUT)
GPIO.setup(DATA, GPIO.OUT)
GPIO.setup(RESET, GPIO.OUT)
GPIO.setup(Pon, GPIO.OUT)

# initialize everything to zero
GPIO.output(W_CLK, False)
GPIO.output(FQ_UD, False)
GPIO.output(DATA, False)
GPIO.output(RESET, False)
GPIO.output(Pon, False)

# Function to send a pulse to GPIO pin
def pulseHigh(pin):
    GPIO.output(pin, True)
    GPIO.output(pin, True)
    GPIO.output(pin, False)
    return
    
# Function to send a byte to AD9850 module
def tfr_byte(data):
    for i in range (0, 8):
        GPIO.output(DATA, data & 0x01)
        pulseHigh(W_CLK)
        GPIO.output(Pon, True)
        data = data >> 1
    return

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = 'some_secret'

users = {
    "admin": "1234",
    "susan": "bye"
}
@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route("/")
@auth.login_required
def main():
   user = auth.username()
   # flash('Welcome %s', % user)   
   return render_template('main.html')
@app.route("/my_form_post", methods=['POST'])

def my_form_post():
    value = request.form['usr'] 
    hz = request.form['val']
    if hz == 'hz':
        hz = 'Hertz'
        mf = 1;    
    elif  hz == 'khz':
        hz = 'Kilo Hertz'
        mf = 1000    
    elif hz == 'mhz':
        hz = 'Mega Hertz'
        mf = 1000000
    start();
    
    message = Markup("<h3>Value: " + value + " " + hz + "</h3>")    
    value = tuningWord(float(value), mf)   
    value = str(value)     
    message += Markup("<h3>Tuning Word: " + value + "</h3>")
    flash(message) 
    return redirect("http://" + ip + "#pigen")

def tuningWord(value, mf):
    freq = int((value*mf) * 4294967296 / 125000000) 
    tw=freq
    GPIO.output(Pon, True)
    for b in range (0, 4):
        tfr_byte(freq & 0xFF)
        freq = freq >> 8
        GPIO.output(Pon, False)
    tfr_byte(0x00)
    pulseHigh(FQ_UD)
    return tw
    
# start the DDS module
def start():
    frequency = int(1000)
    pulseHigh(RESET)
    pulseHigh(W_CLK)
    pulseHigh(FQ_UD)
    tuningWord(frequency,1)
    
# stop the DDS module
def stop():
    pulseHigh(RESET)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
