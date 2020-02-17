from flask import Flask, redirect, url_for, abort, request
import json
import os
import random

from room import Room
from util import format_time

script_path = os.path.dirname(os.path.realpath(__file__))
word_file_path = os.path.join(script_path, 'common-nouns.txt')

app = Flask(__name__)

rooms = []


@app.route('/room/<room_id>')
def show_room(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)

    resp = {
        'id': room.id,
        'created_time': format_time(room.created_time),
    }

    if room.game and room.game.has_started():
        resp.update({'game': room.game.to_json()})

    return resp
    

@app.route('/room', methods=['POST'])
def create_room():
    new_room = Room()
    rooms.append(new_room)
    return redirect(url_for('show_room', room_id=new_room.id))


@app.route('/room/<room_id>/end_turn', methods=['PUT'])
def end_turn(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)

    status = json.loads(request.data)['status']

    if status == 'correct':
        room.game.set_correct()
    else:
        room.game.set_incorrect()
    
    return redirect(url_for('show_room', room_id=room_id))


@app.route('/room/<room_id>/set_word', methods=['PUT'])
def set_word(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)
    
    word = json.loads(request.data)['word']

    room.game.set_word(word)

    return redirect(url_for('show_room', room_id=room_id))


@app.route('/word', methods=['GET'])
def get_word():
    with open(word_file_path, 'r') as f:
        words = (x.strip() for x in f.readlines())
        return {'word': random.choice(words)}


@app.errorhandler(404)
def not_found_error(e):
    return {'error': 'page not found'}, 404


if __name__ == '__main__':
    app.run(debug=True)