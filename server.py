from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

def run():
    app.run(host="0.0.0.0", port=8080)

# Start the dummy server in a separate thread
threading.Thread(target=run, daemon=True).start()
