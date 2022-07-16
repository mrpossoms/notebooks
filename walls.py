#!/usr/bin/env python

import cv2
import numpy as np
import random

r, c = 90, 122
wall = np.zeros((r, c, 3))
mask = np.zeros((r, c, 3))

remaining_board = [
	0,
	(144 * (4 * 2)) * 7,
	(144 * (4 * 8)) * 2,
]


print(remaining_board)
assert(remaining_board[1] + remaining_board[2] >= r * c)

def area(piece):
	return piece[0] * piece[1]

def pieces():
	pieces = [
		(24, 16, 1),
		(24, 32, 1),
		(12, 16, 1),
		(24, 16, 2),
		(24, 32, 2),
		(12, 16, 2),
		(48, 32, 2),
		(32, 48, 2),
		(48, 48, 2),
	]
	random.shuffle(pieces)
	return pieces

def score(r, c, piece):
	a = area(piece)
	scr = max(1, remaining_board[piece[2]]) - a
	other_piece = mask[r][c]

	if other_piece is None:
		return scr + 2

	#if (other_piece == piece).all():
	#	scr -= 1

	scr += abs(area(other_piece) - a) + abs(other_piece[2] - piece[2]) * 1000

	if (other_piece == rotate_piece(piece)).all():
		scr += 1

	#if other_piece[2] != piece[2]:
	#	scr += 1

	scr -= mask[r:r+piece[0], c:c+piece[1]].sum() 

	return scr #np.random.randint(0, 5)

def select_piece(r, c):
	scores = {p:0 for p in pieces()}

	for ri in range(-1, 2):
		for ci in range(-1,2):
			for p in pieces():
				scores[p] += score(r, c, p)

	best = list(scores.keys())[0]

	for p in pieces():
		if scores[best] < scores[p]:
			best = p

	return best

def rotate_piece(piece):
	return (piece[1], piece[0], piece[2])

def set_piece(r, c, piece):
	wall[r:r+piece[0], c:c+piece[1]] = 0
	wall[r+1:r+piece[0]-1, c+1:c+piece[1]-1] = [piece[2] * 64] * 3
	mask[r:r+piece[0], c:c+piece[1]] = piece
	remaining_board[piece[2]] -= area(piece)	

for r in range(wall.shape[0]):
	for c in range(wall.shape[1]):
		# print(mask[r,c])
		if mask[r,c][0] != 0 and mask[r,c][1] != 0:
			continue

		set_piece(r, c, select_piece(r, c))

cv2.imwrite("walls.png", wall)

print(remaining_board)
