from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "bot is on"

def run():
  app.run(host='0.0.0.0',port=8082)

def keep_alive():
    t = Thread(target=run)
    t.start()