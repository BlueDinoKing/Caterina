from flask import Flask, jsonify, render_template
import requests
import json

app = Flask(__name__)

ASSIGNMENTS_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1xj8C0RChSBNRCdC3sOuEv8hz89tcZAu9gfS0d9sbDWw/gviz/tq?tqx=out:json&sheet=Assignments'
CHAPTERS_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1xj8C0RChSBNRCdC3sOuEv8hz89tcZAu9gfS0d9sbDWw/gviz/tq?tqx=out:json&sheet=Chapters'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    response = requests.get(ASSIGNMENTS_SHEET_URL)
    response.raise_for_status()
    json_data = response.text[response.text.find('{'):response.text.rfind('}')+1]
    data = json.loads(json_data)
    assignments = []
    for row in data['table']['rows']:
        assignments.append({
            'name': row['c'][0]['v'],
            'date': row['c'][1]['f'],
            'dependencies': list(map(int, row['c'][2]['v'].split(','))),
            'description': row['c'][3]['v']
        })
    return jsonify(assignments)

@app.route('/api/chapters', methods=['GET'])
def get_chapters():
    response = requests.get(CHAPTERS_SHEET_URL)
    response.raise_for_status()
    json_data = response.text[response.text.find('{'):response.text.rfind('}')+1]
    data = json.loads(json_data)
    chapters = []
    for row in data['table']['rows']:
        chapters.append({
            'number': row['c'][0]['v'],
            'name': row['c'][1]['v']
        })
    return jsonify(chapters)

if __name__ == '__main__':
    app.run(debug=True)