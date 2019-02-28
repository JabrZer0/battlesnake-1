def get_disallowed_coords(data):
	bad_coords = []
	board_dims = [data['board']['height'], data['board']['width']]
	for x in range(board_dims[0]):
		bad_coords.append({'x': x, 'y': -1})
		bad_coords.append({'x': x, 'y': board_dims[1]})

	for y in range(board_dims[1]):
		bad_coords.append({'x': -1, 'y': y})
		bad_coords.append({'x': board_dims[0], 'y': y})

	for segment in data['you']['body']:
		bad_coords.append(segment)

	for snake in data['board']['snakes']:
		for segment in snake['body']:
			bad_coords.append(segment)

	return bad_coords

def get_current_head(data):
	head = {'x': data['you']['body'][0]['x'], 'y': data['you']['body'][0]['y']}
	return head

def get_new_head(data, move):
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

def check_if_risky(data, coord):
	is_risky = True
	head_nearby = False

	for direction in ['up', 'down', 'left', 'right']:
		if get_new_head(coord, direction) not in get_disallowed_coords(data):
			is_risky = False

	for direction in ['up', 'down', 'left', 'right']:
		for snake in data['board']['snakes']:
			if get_new_head(coord, direction) == snake['body'][0] and snake['id'] != data['you']['id']:
				head_nearby = True

	if head_nearby:
		is_risky = True

	return is_risky

def check_if_food(data, coord):
	if coord in data['board']['food']:
		return True
	else: return False