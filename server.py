from flask import Flask, redirect, url_for, abort, request
import json

from room import Room
from util import format_time

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


@app.route('/room/<room_id>', methods=['PUT'])
def update_room(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)

    


@app.errorhandler(404)
def not_found_error(e):
    return {'Error': 'page not found'}, 404


if __name__ == '__main__':
    app.run(debug=True)