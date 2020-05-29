import pyautogui
import time
from PIL import Image

aver_calc_num = 8

def passescondition(color, bias):
    return (color[0]+color[1]+color[2])/3<bias*255

def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return [int(hours),int(mins),int(sec)]

filepath = input('path= ')
color_bias = float(input('color_bias(percentage)= '))
print('top left position:')
input('press enter when ready')
pos1 = pyautogui.position()
screen_x = pos1[0]
screen_y = pos1[1]
print('bottom right position:')
input('press enter when ready')
pos2 = pyautogui.position()
screen_w = pos2[0]-screen_x
screen_h = pos2[1]-screen_y
print('render multiplier:')
res_m = float(input('mult= '))

image = Image.open(filepath)
image_width = image.size[0]
image_height = image.size[1]
res_w = int(screen_w*res_m)
res_h = int(screen_h*res_m)
pixel_ratio_x = image_width/res_w
pixel_ratio_y = image_height/res_h
draw_ratio_x = screen_w/res_w
draw_ratio_y = screen_h/res_h


pixelArray = image.load()
points = []
for y in range(res_h):
    py = y*pixel_ratio_y
    dy = y*draw_ratio_y
    sets = []
    index = -1
    for x in range(res_w):
        px = x*pixel_ratio_x
        dx = x*draw_ratio_x
        if index == -1:#if it does not have a start
            if passescondition(pixelArray[px,py], color_bias):
                index = x
        else:#if it has a start
            if not passescondition(pixelArray[px,py], color_bias):#if it is not what is to be drawn
                sets.append([y, index, x-1])
                index = -1
        if index != -1:
            if x == res_w-1:
                sets.append([y, index, x])
                index = -1
    if len(sets) > 0:
        points.append(sets)
seconds = []
for i in range(len(points)):
    sets = points[i] 
    starttime = time.time()
    
    for set in sets:
        ypos = set[0]
        start = set[1]
        end = set[2]
        pyautogui.moveTo(screen_x+start*draw_ratio_x, screen_y+ypos*draw_ratio_y)
        pyautogui.dragTo(screen_x+end*draw_ratio_x, screen_y+ypos*draw_ratio_y)
    endtime = time.time()
    time_lapsed = endtime - starttime
    seconds.insert(0,time_lapsed)
    if(len(seconds)>aver_calc_num):
        seconds.pop(aver_calc_num-1)
    totalsec_part = 0
    for sec in seconds:
        totalsec_part+=sec
    avgsec = totalsec_part/aver_calc_num
    remainingnum = len(points) - i-1
    totalsec = remainingnum * avgsec
    timestr = time_convert(totalsec)
    print('row [{0}/{1}] {2}:{3}'.format(str(i+1), int(res_h), timestr[1], timestr[2]))

