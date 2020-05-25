from flask import Flask
# make that file called __name__ a flask application
app = Flask(__name__)
# this lines for making the applications is runable by python3 flask_helloWorld.py
if __name__ == '__main__':
    app.run()

# add URL Functionality to the index function( make index function called when requesting url / )
@app.route('/')
def index():
    return "Hello"
