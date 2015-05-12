from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, flash, render_template, request, redirect
from flask import Markup


ip = '192.168.0.4'


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
    name=request.form['usr'] 
    hz=request.form['val']
    if hz=='hz':
        hz='Hertz'    
    elif  hz=='khz':
        hz='Kilo Hertz'    
    elif hz=='mhz':
        hz='Mega Hertz'
        
    
    message = Markup("<h3>Tuning Word: "+hz+"</h3>")
    flash(message) 
    return redirect("http://"+ip+"#pigen")



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
