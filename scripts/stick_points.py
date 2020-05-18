#!/usr/bin/python3

import math, sys
import gc_to_n64

def gen_gc_stick_points(min_radius, max_radius, step_width):

    points  = []

    radius = min_radius

    while (radius <= max_radius):
        start_x = 0
        end_x = int(math.sqrt((radius*radius) / 2))

        m = gc_to_n64.GC_EDGE_SLOPE
        b = radius

        for x in range(start_x, end_x + 1):
            y = round(m*x + b)
            points.append((x,y))

        radius = radius + step_width

    flipped_points = []
    for p in points:
        flipped_points.append((p[1], p[0]))

    points = points + flipped_points

    flipped_points = []
    for p in points:
        flipped_points.append((p[0], -p[1]))

    points = points + flipped_points

    flipped_points = []
    for p in points:
        flipped_points.append((-p[0], p[1]))

    points = points + flipped_points

    return points


def transform_to_n64_points(gc_points):
    transformed_points = []
    for p in gc_points:
        new_p = gc_to_n64.gc_to_n64_transform(p[0], p[1])
        transformed_points.append(new_p)

    return transformed_points


if len(sys.argv) < 2:
    print('Please specify "input" or "output"')
else:
    io = sys.argv[1]

    gc_points = gen_gc_stick_points(5, 105, 10)

    if io == 'input':
        print('x,y')
        for p in gc_points:
            print('%d,%d' % (p[0], p[1]))
    elif io == 'output':
        print('x,y')
        for p in transform_to_n64_points(gc_points):
            print('%d,%d' % (p[0], p[1]))
    else:
        print('%s is no a valid option')
