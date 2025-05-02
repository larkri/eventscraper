from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('polisen_data.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/filter/<event_type>')
def filter_event(event_type):
    data = load_data()
    filtered_data = [event for event in data if event['event_type'] == event_type]
    return jsonify(filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
