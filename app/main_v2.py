import json
import os
import random
import bottle
import operator
from utils_v2 import get_disallowed_coords, get_current_head, get_possible_states, get_new_head

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#FF0000"

    return start_response(color)

# ************** THIS IS THE BIG ONE *********************
@bottle.post('/move')
def move():
    data = dict(bottle.request.json)
    current_head = get_current_head(data)
    bad_moves = get_disallowed_coords(data)
    directions = ['up', 'left', 'down', 'right']

    # get a list of possible states next turn
    next_turn_states = get_possible_states(data)
    # for each possible state
    for state in next_turn_states:
        # if it didn't end the game
        if state[1]:
            # generate a list of the NEXT possible states based on that one
            temp_states = get_possible_states(state[1])
            # convert them all to booleans to save memory (because we don't care about the directions of the future states, just how many result in death)
            state[1] = [bool(state[1])]
            state[1].extend([bool(x[1]) for x in temp_states])
        # count the number of options we have for each player move
            state[1] = sum(state[1])

        else:
            state[1] = 0


    direction_values = {'up': 0, 'left': 0, 'down': 0, 'right': 0, }

    for direction in directions:
        for next_turn_state in next_turn_states:
            if next_turn_state[0] == direction:
                direction_values[direction] = direction_values[direction] + next_turn_state[1]

    move_decision = max(direction_values.items(), key=operator.itemgetter(1))[0]
    print(data['turn'], current_head, direction_values, move_decision)

    if data['you']['health'] < 50:
        for direction in direction_values:
            if get_new_head(data, direction) in data['board']['food']:
                move_decision = direction

    return move_response(move_decision)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    # print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
