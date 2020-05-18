#!/usr/bin/python3

import math, sys

GC_EDGE_SLOPE = (0.7071067812 - 1.0) / 0.7071067812
N64_EDGE_SLOPE = (0.875 - 1.0) / 0.875

def _normalize_gc(val):
    return float(val) / 105.0

def _denormalize_n64(val):
    return round(val * 80.0)

def gc_to_n64_transform(gc_x, gc_y):
    gc_x = _normalize_gc(gc_x)
    gc_y = _normalize_gc(gc_y)

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
        new_y = y
        new_x = 0
    else:
        slope = y / x

        intersect_x = 1.0 / (slope - GC_EDGE_SLOPE)
        intersect_y = (GC_EDGE_SLOPE * intersect_x) + 1.0

        dist_sq1 = (intersect_x * intersect_x) + (intersect_y * intersect_y)

        intersect_x = 1.0 / (slope - N64_EDGE_SLOPE)
        intersect_y = (N64_EDGE_SLOPE * intersect_x) + 1.0

        dist_sq2 = (intersect_x * intersect_x) + (intersect_y * intersect_y)

        scale_sq = dist_sq2 / dist_sq1
        dist_sq = ((x * x) + (y * y))

        scale_sq = ((scale_sq - 1) * dist_sq) + 1

        dist_sq = dist_sq * scale_sq

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

    new_x = _denormalize_n64(new_x)
    new_y = _denormalize_n64(new_y)

    return (new_x, new_y)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Please specify exactly two numbers')
        sys.exit(1)

    try:
        in_x = float(sys.argv[1])
        in_y = float(sys.argv[2])
    except:
        print('Could not parse provided values as numbers')

    (out_x, out_y) = gc_to_n64_transform(in_x, in_y)

    print("(" + str(out_x) + ", " + str(out_y) + ")")
