from __future__ import print_function
import sys
import time
import tiling_dino

filename = "test0.txt"

fp = open(filename, 'r')
lines = fp.readlines()

result = tiling_dino.tile_image(lines)

for i in range(len(result)):
    print(result[i])