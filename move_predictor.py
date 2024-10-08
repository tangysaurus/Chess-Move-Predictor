import csv, numpy as np
from numpy.linalg import matrix_power

# Store column data in arrays
with open('Carlsen_moves.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter = ',')
	game_id, moves = [], []
	next(csv_reader)

	for row in csv_reader:
		game_id.append(row[0])
		moves.append(row[1] + row[2])

# Store connection frequencies between current move sequence and next move
def find_connections():
	connections = {}
	cur = ""
	for i in range(120):
		if i > 0 and game_id[i] != game_id[i-1]:
			cur = ""
		if cur not in connections:
			connections[cur] = {cur + moves[i] : 1, "n" : 1}
		else:
			if moves[i] not in connections[cur]:
				connections[cur][cur + moves[i]] = 1
			else:
				connections[cur][cur + moves[i]] += 1
			connections[cur]["n"] += 1
		cur += moves[i]
	return connections

# Calculate relative frequencies
def relative_freq(connections):
	for seq in connections:
		for move in connections[seq]:
			if move != "n":
				connections[seq][move] /= connections[seq]["n"]
	return connections

# Create a transition matrix
def transition_matrix(probabilities):
	states = set()
	for seq in probabilities:
		states.add(seq)
		for move in probabilities[seq]:
			states.add(move)

	transition = []
	states = list(states)
	states_to_id = {}

	for i in range(len(states)):
		states_to_id[states[i]] = i

	for state in states:
		if state not in probabilities:
			transition.append([0] * len(states))
		else:
			cur = []
			for i in range(len(states)):
				if states[i] == state or states[i] not in probabilities[state]:
					cur.append(0)
				else:
					cur.append(probabilities[state][states[i]])
			transition.append(cur)
	return transition, states_to_id

# Find the probability of going from position a to b in n steps
def a_to_b(a, b, n, transition, states_to_id):
	return matrix_power(transition, n)[states_to_id[a]][states_to_id[b]]

# Generate the most probable n step walk from a specific position
def probable_walk(origin, n):
	res = 1
	for i in range(n):
		max_prob = 0
		max_move = ""
		for move in connections[origin]:
			if move != "n":
				if connections[origin][move] > max_prob:
					max_prob = connections[origin][move]
					max_move = move
		res *= max_prob
		origin = max_move
	return res

connections = find_connections()
probabilities = relative_freq(connections)
walk = probable_walk("d2d4", 10)
transition, states_to_id = transition_matrix(probabilities)