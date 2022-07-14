#!/usr/bin/env python

import cv2
import numpy as np

r, c = 12 * 10, 12 * 10
wall = np.zeros((r, c, 3))
mask = [[None] * c for _ in range(r)]

print(mask)

def pieces():
	return [
		(24, 16, 1),
		(24, 32, 1),
		(12, 16, 1),
		(24, 16, 2),
		(24, 32, 2),
		(12, 16, 2),
	]

def rotate_piece(piece):
	return (piece[1], piece[0], piece[2])

def set_piece(r, c, piece):
	wall[r:piece[0], c:piece[1]] = piece[2]
	mask[r][c] = piece

cv2.imwrite("walls.png", wall)
