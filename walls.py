#!/usr/bin/env python

import cv2
import numpy as np
import random
import collections
import shutil, os

r, c = 90, 122

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

def score(mask, remaining_board, r, c, piece):
	a = area(piece)
	scr = max(1, remaining_board[piece[2]] - a)
	other_piece = mask[r][c]

	if other_piece is None:
		return scr

	scr += abs(area(other_piece) - a) + abs(other_piece[2] - piece[2]) * 1000

	if (other_piece == piece).all():
		scr -= a

	if other_piece[2] == piece[2]:
		scr -= a / 2

	# if this region already has pieces in it super demote
	# piece that overlaps existing pieces
	scr -= mask[r:r+piece[0], c:c+piece[1]].sum()

	return scr #np.random.randint(0, 5)

def select_piece(mask, remaining_board, r, c):
	scores = {p:0 for p in pieces()}

	for ri in range(-1, 2):
		for ci in range(-1,2):
			for p in pieces():
				scores[p] += score(mask, remaining_board, r + ri, c + ci, p)

	best = list(scores.keys())[0]
	for p in pieces():
		if scores[best] < scores[p]:
			best = p

	return scores[best], best

def rotate_piece(piece):
	return (piece[1], piece[0], piece[2])

def set_piece(wall, mask, remaining_board, r, c, piece):
	wall[r:r+piece[0], c:c+piece[1]] = 0
	wall[r+1:r+piece[0]-1, c+1:c+piece[1]-1] = [piece[2] * 64] * 3
	mask[r:r+piece[0], c:c+piece[1]] = piece
	remaining_board[piece[2]] -= area(piece)	

def generate(wall, mask, remaining_board):
	score = 0
	placement = {}

	for r in range(wall.shape[0]):
		for c in range(wall.shape[1]):
			# print(mask[r,c])
			if mask[r,c][0] != 0 and mask[r,c][1] != 0:
				continue

			piece_score, piece = select_piece(mask, remaining_board, r, c)
			set_piece(wall, mask, remaining_board, r, c, piece)

			if piece in placement:
				placement[piece] += 1
			else:
				placement[piece] = 1

			score += piece_score

	score -= len(placement)

	return score, placement


def generate_candidates():
	candidates = collections.OrderedDict()

	for _ in range(10):
		wall = np.zeros((r, c, 3))
		mask = np.zeros((r, c, 3))

		remaining_board = [
			0,
			(144 * (4 * 2)) * 7,
			(144 * (4 * 8)) * 2,
		]

		score, placement = generate(wall, mask, remaining_board)
		candidates[score] = wall, placement

	shutil.rmtree('walls', ignore_errors=True)
	shutil.rmtree('placements', ignore_errors=True)

	try:
		os.mkdir('walls')
		os.mkdir('placements')
	except:
		pass

	i = 0
	for score in reversed(sorted(candidates)):
		wall, placement = candidates[score]

		cv2.imwrite(f"walls/{i}.{score}.png", wall)

		with open(f"placements/{i}.{score}.txt", "w+") as fp:
			for piece in placement:
				fp.write(f'{str(piece)}: {placement[piece]}\n')

		i += 1



random.seed(0)
generate_candidates()
