from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, flash, render_template, request, redirect
from flask import Markup
import math
from lib2to3.fixer_util import String


ip = '192.168.0.4'
defClock = 125000000

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
   user =  auth.username()
   #flash('Welcome %s', % user)   
   return render_template('main.html')
@app.route("/my_form_post", methods=['POST'])
def my_form_post():
    value=request.form['usr'] 
    hz=request.form['val']
    if hz=='hz':
        hz='Hertz'
        mf=1;    
    elif  hz=='khz':
        hz='Kilo Hertz'
        mf=1000    
    elif hz=='mhz':
        hz='Mega Hertz'
        mf=1000000
    
    message = Markup("<h3>Value: "+value+" "+hz+"</h3>")    
    value = tuningWord(float(value),mf)   
    value = str(value)
    print value  
    message+= Markup("<h3>Tuning Word: "+value+"</h3>")
    flash(message) 
    return redirect("http://"+ip+"#pigen")

def tuningWord(value,mf):
    tw= (value*mf)* (math.pow(2, 32) / defClock)
    return tw

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
