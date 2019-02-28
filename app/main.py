import json
import os
import random
import bottle
from utils import get_disallowed_coords, get_current_head, get_new_head, check_if_risky, check_if_food

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

    color = "#00FF00"

    return start_response(color)

# ************** THIS IS THE BIG ONE *********************
@bottle.post('/move')
def move():
    data = dict(bottle.request.json)
    bad_moves = get_disallowed_coords(data)

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(data['game'])

    directions = ['up', 'down', 'left', 'right']
    risky_directions = []
    non_risky_directions = []
    food_directions = []
    directions_info = {'bad': ['up', 'down', 'left', 'right'],
                        'risky': [],
                        'risky_food': [],
                        'non_risky': [],
                        'non_risky_food': []}
    move_check = False
    count = 0

    for direction in directions:
        new_head = get_new_head(data, direction)
        is_risky = check_if_risky(data, new_head)
        has_food = check_if_food(data, new_head)

        if new_head not in bad_moves:
            directions_info['risky'].append(direction)
            if has_food:
                directions_info['risky_food'].append(direction)

        if new_head not in bad_moves and not is_risky:
            directions_info['non_risky'].append(direction)
            if has_food:
                directions_info['non_risky_food'].append(direction)

    if len(directions_info['non_risky_food']) > 0:
        print('Turn' + str(data['turn']) + ': non-risky-food option available for ' + data['you']['name'])
        return move_response(random.choice(directions_info['non_risky_food']))

    if len(directions_info['non_risky']) > 0:
        print('Turn' + str(data['turn']) + ': non-risky option available for ' + data['you']['name'])
        return move_response(random.choice(directions_info['non_risky']))

    if len(directions_info['risky_food']) > 0:
        print('Turn' + str(data['turn']) + ': risky-food option available for ' + data['you']['name'])
        return move_response(random.choice(directions_info['risky_food']))

    if len(directions_info['risky']) > 0:
        print('Turn' + str(data['turn']) + ': risky option available for ' + data['you']['name'])
        return move_response(random.choice(directions_info['risky']))

    print('Turn' + str(data['turn']) + ': no options available for ' + data['you']['name'])
    return move_response('up')


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
