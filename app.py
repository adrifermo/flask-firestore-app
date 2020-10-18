# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import logging

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB

cred = credentials.Certificate("serviceAccountKey.json")
default_app = initialize_app(cred)
db = firestore.client()
collection = db.collection('devfest')

@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:

        logging.info(request)

        id = request.json['id']
        title = request.json['title']
        description = request.json['description']
        speaker = request.json['speaker']

        data = {
            'description': description,
            'title': title,
            'speaker': speaker
        }

        collection.document(id).set(data)

        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return "An Error Occured:"

@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query

        todo_id = request.args.get('id')
        if todo_id:
            todo = collection.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in collection.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        print(e)
        return "An Error Occured:"

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        collection.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return "An Error Occured:"

@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        collection.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        print(e)
        return "An Error Occured:"

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
