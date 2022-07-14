#!/usr/bin/env python3

import numpy as np
import random
import cv2

BASE = 10
PAD = 1
F = np.zeros((128, 128))

def rotate(l, n):
    n = n % len(l)
    return l[n:] + l[:n]

def sine_fib(t):

    fib = [1, 1, 2, 3 ]
    return rotate(fib, int(np.sin(t) * len(fib)))

def rand_fib(c):

    fib = [1, 1, 2, 3 ]
    random.shuffle(fib)
    return fib
    #return rotate(fib, c)

def seq_bits(seq):
    bits = []

    for i in seq:
        bits += [1] * (i * BASE)
        bits += [0] * PAD

    return bits


def rand_fib_planks(F):
    c = 0
    while c < F.shape[1] - 1:
        r = 1
        fib = rand_fib(c//2) 
        bits = seq_bits(fib)
        to_pop = np.random.randint(0, fib[0]*BASE//2)
        for _ in range(to_pop):
            bits.pop()

        while r < F.shape[0] - 1:
            if len(bits) == 0:
                bits = seq_bits(rand_fib(c//2))

            F[r][c] = bits.pop() * 255   
            r += 1

        c += 2

def fib_wave(F):
    c = 0
    while c < F.shape[1] - 1:
        r = 1
        fib = sine_fib(c * np.pi / 8) 
        bits = seq_bits(fib)
        to_pop = 0 #np.random.randint(0, fib[0]*BASE//2)
        for _ in range(to_pop):
            bits.pop()

        while r < F.shape[0] - 1:
            if len(bits) == 0:
                bits = seq_bits(sine_fib(c * np.pi / 8))

            F[r][c] = bits.pop() * 255   
            r += 1

        c += 2


#fib_wave(F)
rand_fib_planks(F)

cv2.imwrite("floor.png", F)
