import numpy as np
import json
import pdb

def makeGcode(cal, sp, side):
    """
    creates a gcode for the calibration
    Now made just for a 10 cm thickness block
    sp = start point in x, y, z. Lower left side of the milling
    """
    fr = ' F500' # feedrate
    r = 12.5 # tool radius
    start_x = - 47.0/2.0 # the most left value when gcode is around x = 0
    half_material = 100.0/2.0 # the half distance of the material thickness (hardcoded for 10 cm material)
    # cut_z[0] == coordinate to the end-milling of the side of the cube (hardcoded)
    # cut_z[1] == coordinate to the top of the cube
    if side == 'top':
        cut_z = [-150.1 - r, cal[1] - (half_material - sp[2])]
    if side == 'bottom':
        cut_z = [-50.1 - r, cal[1] + (half_material + sp[2])]

    lines = []
    # a coordinate over the starting point
    # note that 30.0 is the cube height
    lines.append([start_x, sp[1] + 30.0, 0.1])
    
    # vertical (left) side of the cube
    lines.append([start_x, sp[1] + 30.0, cut_z[0]])
    lines.append([start_x, sp[1], cut_z[0]])
    lines.append([start_x, sp[1], cut_z[1]])
    
    # horizontal side of the cube
    x = start_x + 1
    y = sp[1]
    z = cut_z[1]
    dx = 0.0
    dy = np.array([0, 30.0])
    for i in range(22):
        lines.append([x + dx + r, y + dy[i%2], z])
        lines.append([x + dx + r, y + dy[(i+1)%2], z])
        dx = dx + 1

    # vertical (right) side of the cube
    lines.append([start_x + dx + 2*r, sp[1], cut_z[1]])
    lines.append([start_x + dx + 2*r, sp[1], cut_z[0]])
    lines.append([start_x  + dx + 2*r, sp[1] + 30.0, cut_z[0]])
    lines.append([start_x + dx + 2*r, sp[1] + 30.0, 0.1])
    
    # offset in x depending on side
    if side == 'top':
        for i in range(len(lines)):
            lines[i][0] = lines[i][0] + cal[0] - sp[0]
    if side == 'bottom':
        for i in range(len(lines)):
            lines[i][0] = lines[i][0] + cal[0] + sp[0]

    # lines to gcode
    gcode = ''
    for line in lines:
        gcode = gcode + 'G1'
        gcode = gcode + ' X'+str(line[0])
        gcode = gcode + ' Y'+str(line[1])
        gcode = gcode + ' Z'+str(line[2])
        gcode = gcode + fr 
        gcode = gcode + '\n' 

    if side == 'top':
        with open('cal_top.gc', 'w') as f:
            f.writelines(gcode)
    if side == 'bottom':
        with open('cal_bottom.gc', 'w') as f:
            f.writelines(gcode)


#--- SCRIPT ---#
# read the calibration setting
with open('../settings.json', 'r') as f:
    data = json.load(f)
calibration = data['MachineRotCenter']

# the offset of the milling. 
# x is offset from center of rotation, where the milling should be
# y is offset zero, where the milling should be
# z is offset from center of rotation, the height of the cube to be milled
offset = np.array([100.0, 1000.0, 30.0])
# make gcode for top
# offset_top = np.array([cal[0] - offset[0], offset[1], cal[1] + offset[2]]) 
makeGcode(calibration, offset, 'top')
# make gsode for bottom
# offset_bottom = np.array([cal[0] + offset[0], offset[1], cal[1] - offst[2]]) 
makeGcode(calibration, offset, 'bottom')
