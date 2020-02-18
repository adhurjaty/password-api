from flask import Flask, redirect, url_for, abort, request
import json
import os
import random

from player import Player
from room import Room
from team import Team
from util import format_time

script_path = os.path.dirname(os.path.realpath(__file__))
word_file_path = os.path.join(script_path, 'common-nouns.txt')

app = Flask(__name__)

rooms = []


@app.route('/room/<player_id>')
def show_room(player_id):
    room = next((r for r in rooms if r.has_player(player_id)), None)
    if not room:
        abort(404)

    resp = {
        'id': room.id,
        'created_time': format_time(room.created_time),
    }

    if room.game and room.game.has_started():
        resp.update({'game': room.game.to_json(player_id)})

    return resp
    

@app.route('/room', methods=['POST'])
def create_room():
    new_room = Room()
    rooms.append(new_room)

    parsed_req = json.loads(request.data)
    player = Player(parsed_req['name'])
    try:
        new_room.add_player(player)
    except Exception as e:
        return {'error': str(e)}, 422

    return {
        'id': new_room.id,
        'player_id': player.id
    }


@app.route('/room/<player_id>', methods=['PUT'])
def end_turn(player_id):
    room = next((r for r in rooms if r.has_player(player_id)), None)
    if not room:
        abort(404)

    parsed_req = json.loads(request.data)

    if 'answer_status' in parsed_req: 
        if parsed_req['answer_status'] == 'correct':
            room.game.set_correct()
        else:
            room.game.set_incorrect()
    if 'word' in parsed_req:
        room.game.set_word(parsed_req['word'])
    if 'teams' in parsed_req:
        room.start_game(parsed_req['teams'])
    
    return redirect(url_for('show_room', player_id=player_id))


@app.route('/room/<room_id>/add_player', methods=['PUT'])
def add_player(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)

    parsed_req = json.loads(request.data)

    player = Player(parsed_req['name'])
    try:
        room.add_player(player)
    except Exception as e:
        return {'error': str(e)}, 422

    return {'name': player.name, 'id': player.id}

@app.route('/word', methods=['GET'])
def get_word():
    with open(word_file_path, 'r') as f:
        words = (x.strip() for x in f.readlines())
        return {'word': random.choice(words)}


@app.route('/room/<room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = next((r for r in rooms if r.id == room_id), None)
    if not room:
        abort(404)

    rooms.remove(room)

    return {'status': 'success'}


@app.errorhandler(404)
def not_found_error(e):
    return {'error': 'page not found'}, 404


if __name__ == '__main__':
    app.run(debug=True)