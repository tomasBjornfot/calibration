import numpy as np
import matplotlib.pyplot as plt
import pdb

# --- FUNCTIONS ---#
def dataToGcode(points, feedrate):
    sf = ' F'+str(feedrate)
    lines = []
    for i in range(len(points)):
        sx = 'X'+str(points[i][0])
        sy = ' Y'+str(points[i][1])
        sz = ' Z'+str(points[i][2])
        lines.append('G1 '+sx+sy+sz+sf)
    return lines

def writeFile(filename, lines):
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line+'\n')

def square(center, x_width, no_patches, patch_distance):
    x = center[0] - x_width/2.0 
    y = center[1] + (no_patches*patch_distance)/2.0
    z = center[2]
    
    data = []
    for i in range(no_patches):
        data.append([x, y, z])
        if i%2 == 0:
            x = x + x_width
        else:
            x = x - x_width
        data.append([x, y, z])
        y = y - patch_distance
    return data

# --- SCRIPT --- #
x_offset= -200
y_offset = 1200
# DECK
pts = []
# making the cut for the horizontal plane
for z in [40, 30, 20]: 
    sq = square([x_offset, y_offset, z], 100, 21, 5)
    for s in sq:
        pts.append(s) 
# making the cut for the vertical plane
for z in [10, 0, -10, -20]:
    sq = square([x_offset - 25, y_offset, z], 50, 21, 5)
    for s in sq:
        pts.append(s) 
lines = dataToGcode(pts, 1000)
writeFile('../cam/calibrate_1.gc', lines)


# BOTTOM 
pts = []
# making the cut for the horizontal plane
for z in [40, 30, 20]: 
    sq = square([-x_offset, y_offset, z], 100, 21, 5)
    for s in sq:
        pts.append(s) 
# making the cut for the vertical plane
for z in [10, 0, -10, -20]:
    sq = square([-x_offset + 25, y_offset, z], 50, 21, 5)
    for s in sq:
        pts.append(s) 
lines = dataToGcode(pts, 1000)
writeFile('../cam/calibrate_2.gc', lines)



