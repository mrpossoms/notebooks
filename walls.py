#!/usr/bin/env python

import cv2
import numpy as np
import random
import collections
import shutil, os

r, c = 90, 122

def area(piece):
	return piece[0] * piece[1]

def volume(piece):
	return piece[0] * piece[1] * piece[2]

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
	a = volume(piece)
	scr = min(1, remaining_board[piece[2]] - a)
	other_piece = mask[r][c]

	# penalize for overlapping space that contains pieces that have been set
	scr += -mask[r:r+piece[0], c:c+piece[1]].sum()

	# if scr < 0:
	# 	return scr

	scr += (abs(volume(other_piece) - a))

	if (other_piece == np.array([0, 0, 0])).all():
		return scr


	 # + (abs(other_piece[2] - piece[2]) * 10000)


	# scr += (abs(other_piece[2] - piece[2]) * a)

	# if other_piece[2] == piece[2]:
	# 	scr -= a / 2

	# if this region already has pieces in it super demote
	# piece that overlaps existing pieces


	return scr #np.random.randint(0, 5)

def select_piece(mask, remaining_board, r, c):
	scores = {p:0 for p in pieces()}

	if random.random() < 0.125:
		for _ in range(3):
			p = pieces()[0]
			s = score(mask, remaining_board, r, c, p)
			if s > 0:
				return s, p

	for ri in range(-1, 2):
		for ci in range(-1,2):
			print(f'{ri},{ci}: {mask[r + ri, c + ci]}')
			for p in pieces():
				s = score(mask, remaining_board, r + ri, c + ci, p)
				print(f'\t{p}: {s}')
				scores[p] += s

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
	placement_score = 0
	placement = {}

	for r in range(wall.shape[0]):
		for c in range(wall.shape[1]):
			# print(mask[r,c])
			if mask[r,c][0] != 0 and mask[r,c][1] != 0:
				continue

			piece_score, piece = None, None

			if r == 0 and c == 0:
				piece = pieces()[0]
				piece_score = score(mask, remaining_board, r, c, piece)
			else:
				piece_score, piece = select_piece(mask, remaining_board, r, c)

			set_piece(wall, mask, remaining_board, r, c, piece)

			if piece in placement:
				placement[piece] += 1
			else:
				placement[piece] = 1

			placement_score += piece_score

			# if len(placement) == 2:
			# 	return 0, placement

	placement_score -= len(placement)

	return placement_score, placement


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
