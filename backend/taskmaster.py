from flask import Flask, request, jsonify, json
import sqlite3
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_db():
    conn = sqlite3.connect('taskmaster.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT,
                description TEXT)''')
    conn.commit()
    conn.close()
    return

def check_string(string):
    if string is None:
        return False
    return bool(re.match("^[a-zA-Z0-9 -]+$", string))

def check_id(id):
    if id is None:
        return False
    return bool(re.match("^[0-9]+$", id))

@app.route('/')
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = []
    try:
        with sqlite3.connect("taskmaster.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            for row in cursor.fetchall():
                tasks.append({'id': row[0], 'title': row[1], 'description': row[2]})
    except:
        tasks = []
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    title = json.loads(request.data).get('title')
    description = json.loads(request.data).get('description')
    #check if title is empty
    if title == '' or description == '':
        return jsonify({'status': 'failure', 'error': 'Missing title or description'})
    
    if(not check_string(title)):
        return jsonify({'status': 'failure', 'error': 'Invalid Task Name'})
    
    if(not check_string(description)):
        return jsonify({'status': 'failure', 'error': 'Invalid Task Description'})
    answer = {}
    try:
        with sqlite3.connect("taskmaster.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
            conn.commit()
            inserted_id = cursor.lastrowid
            answer = jsonify({'status': 'success', 'id': inserted_id})
    except:
        conn.rollback()
        answer = jsonify({'status': 'failure', 'error': 'Could not create task'})
    finally:
        conn.close()
    return answer
    
@app.route('/tasks/<task_id>/complete', methods=['DELETE'])
def complete_task(task_id):
    if not check_id(task_id):
        return jsonify({'status': 'failure', 'error': 'Invalid id'})
    
    answer = {}
    try:
        with sqlite3.connect("taskmaster.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.commit()
            answer = jsonify({'status': 'success'})
    except:
        conn.rollback()
        answer = jsonify({'status': 'failure', 'error': 'Could not delete task'})
    finally:
        conn.close()
    return answer

if __name__ == '__main__':
    create_db()
    app.run(port=5000, debug=True)