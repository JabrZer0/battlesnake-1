from itertools import product
from copy import deepcopy
from time import time

def get_disallowed_coords(data):
	bad_coords = []
	board_dims = [data['board']['height'], data['board']['width']]
	for x in range(board_dims[0]):
		bad_coords.append({'x': x, 'y': -2})
		bad_coords.append({'x': x, 'y': board_dims[1] + 1})

	for y in range(board_dims[1]):
		bad_coords.append({'x': -2, 'y': y})
		bad_coords.append({'x': board_dims[0] + 1, 'y': y})

	for segment in data['you']['body']:
		bad_coords.append(segment)

	for snake in data['board']['snakes']:
		for segment in snake['body']:
			bad_coords.append(segment)

	return bad_coords

def get_current_head(data): # gets the current PLAYER head
	head = {'x': data['you']['body'][0]['x'], 'y': data['you']['body'][0]['y']}
	return head

def get_new_head(data, move): # data can be either the full gamestate or a single location
	if len(data) != 2:
		current_head = get_current_head(data)
	else:
		current_head = data

	new_head = {'x': current_head['x'], 'y': current_head['y']}

	if move == 'left':
		new_head['x'] = current_head['x'] - 1

	if move == 'right':
		new_head['x'] = current_head['x'] + 1

	if move == 'up':
		new_head['y'] = current_head['y'] - 1

	if move == 'down':
		new_head['y'] = current_head['y'] + 1

	return new_head

def get_possible_moves(current_head, bad_moves):
	possible_moves = {'up': False, 'left': False, 'down': False, 'right': False}
	for direction in ['up', 'left', 'down', 'right']:
		if get_new_head(current_head, direction) not in bad_moves:
			possible_moves[direction] = True
	return possible_moves

def update_snake(data, snake_id, move): # creates an edited copy of the input data, or returns false if snake dies
	temp_data = deepcopy(data)
	for snake in temp_data['board']['snakes']:
		if snake['id'] == snake_id:
			old_head = {'x': snake['body'][0]['x'], 'y': snake['body'][0]['y']}
			new_head = get_new_head(old_head, move)

			if new_head in get_disallowed_coords(data):
				return False

			snake['body'].insert(0, new_head)
			if new_head not in data['board']['food']:
				snake['body'] = snake['body'][:-1]
	return temp_data

def update_board(data, all_snake_moves): # moves should be formatted as {<id>:<move>, ...}
	temp_data = deepcopy(data)
	for snake in temp_data['board']['snakes'] + [temp_data['you']]:
		update = update_snake(temp_data, snake['id'], all_snake_moves[snake['id']])
		if not update:
			if snake['id'] != data['you']['id']:
				temp_data['board']['snakes'].remove(snake)
			else:
				print(snake['body'][0], 'Snake dies at: ', all_snake_moves[snake['id']])
				return False
		else:
			temp_data = update

	return temp_data

def get_possible_states(data):  # returns a set of all possible moves: False for a losing move, or a new board state
	
	# generate a list of all possible moves given snakes and moves for each snake
	ids = [x['id'] for x in data['board']['snakes']]
	dimensions = ['up', 'left', 'down', 'right']
	results = []

	dim_combinations = list(product(dimensions, repeat=len(ids)))
	states = []
	for i in range(len(dim_combinations)):
		states.append({})
		for j in range(len(ids)):
			states[i][ids[j]] = dim_combinations[i][j]

	for i in range(len(states)): # gives a set of [[player_move, board position], ...]
		results.append([states[i][data['you']['id']], update_board(data, states[i])]) # DEBUG: everything works correctly up to this point. This line is the issue

	return results

