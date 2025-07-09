from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = {}

    # ✅ Handle ping event from GitHub
    if request.headers.get('X-GitHub-Event') == 'ping':
        return jsonify({"message": "Ping received"}), 200

    # ✅ Parse Push Event
    if 'commits' in data:
        event['type'] = 'push'
        event['author'] = data['pusher']['name']
        event['from_branch'] = data['ref'].split('/')[-1]
        event['timestamp'] = datetime.now(pytz.utc)

    # ✅ Parse Pull Request Event
    elif 'pull_request' in data:
        event['type'] = 'pull_request'
        event['author'] = data['pull_request']['user']['login']
        event['from_branch'] = data['pull_request']['head']['ref']
        event['to_branch'] = data['pull_request']['base']['ref']
        event['timestamp'] = datetime.now(pytz.utc)

    else:
        return jsonify({"message": "Unsupported event"}), 400

    collection.insert_one(event)
    return jsonify({"message": "Event stored"}), 200

@app.route('/data')
def data():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
        e['timestamp'] = e['timestamp'].isoformat()
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
# test webhook trigger
# webhook test line 2
# Triggering webhook test



