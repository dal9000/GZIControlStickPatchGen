#!/usr/bin/python3

import math, sys

GC_EDGE_SLOPE = (0.7071067812 - 1.0) / 0.7071067812
N64_EDGE_SLOPE = (0.875 - 1.0) / 0.875

def normalize_gc(val):
    return val / 106

def denormalize_n64(val):
    return val * 80

def gc_to_n64_transform(gc_x, gc_y):
    x = gc_x
    if (gc_x < 0):
        x = -x   

    y = gc_y
    if (gc_y < 0):
        y = -y

    swapped = False
    if (y < x):
        swapped = True
        temp = y
        y = x
        x = temp

    if x == 0:
        return (gc_x, gc_y)

    slope = y / x

    intersect_x = 1.0 / (slope - GC_EDGE_SLOPE)
    intersect_y = (GC_EDGE_SLOPE * intersect_x) + 1.0

    dist_sq1 = (intersect_x * intersect_x) + (intersect_y * intersect_y)

    intersect_x = 1.0 / (slope - N64_EDGE_SLOPE)
    intersect_y = (N64_EDGE_SLOPE * intersect_x) + 1.0

    dist_sq2 = (intersect_x * intersect_x) + (intersect_y * intersect_y)

    scale_sq = dist_sq2 / dist_sq1

    dist_sq = ((x * x) + (y * y)) * scale_sq

    new_x = math.sqrt(dist_sq / ((slope * slope) + 1))
    new_y = slope * new_x

    if swapped:
        temp = new_y
        new_y = new_x
        new_x = temp

    if (gc_x < 0):
        new_x = -new_x    

    if (gc_y < 0):
        new_y = -new_y

    return (new_x, new_y)


in_x = float(sys.argv[1])
in_y = float(sys.argv[2])

(x, y) = gc_to_n64_transform(normalize_gc(in_x), normalize_gc(in_y))

print("(" + str(round(denormalize_n64(x))) + ", " + str(round(denormalize_n64(y))) + ")")
