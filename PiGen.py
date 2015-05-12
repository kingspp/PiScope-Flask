from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask, flash, render_template, request

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
