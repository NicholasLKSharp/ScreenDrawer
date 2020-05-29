import pyautogui
from PIL import Image

def passescondition(color, bias):
    return (color[0]+color[1]+color[2])/3<bias*255

filepath = input('path= ')
color_bias = float(input('color_bias(percentage)= '))
print('position on screen:')
screen_x = int(input('x= '))
screen_y = int(input('y= '))
print('size on screen:')
screen_w = int(input('width= '))
screen_h = int(input('height= '))
print('render multiplier:')
res_m = float(input('mult= '))

image = Image.open(filepath)
image_width = image.size[0]
image_height = image.size[1]
res_w = int(screen_w*res_m)
res_h = int(screen_w*res_m)
pixel_ratio = image_width/res_w
draw_ratio = screen_w/res_w


pixelArray = image.load()
points = []
for y in range(res_h):
    py = y*pixel_ratio
    dy = y*draw_ratio
    sets = []
    index = -1
    for x in range(res_w):
        px = x*pixel_ratio
        dx = x*draw_ratio
        if index == -1:#if it does not have a start
            if passescondition(pixelArray[dx,dy], color_bias):
                index = x
        else:#if it has a start
            if not passescondition(pixelArray[dx,dy], color_bias):#if it is not what is to be drawn
                sets.append([y, index, x-1])
                index = -1
        if index != -1:
            if x == res_w-1:
                sets.append([y, index, x])
                index = -1
    if len(sets) > 0:
        points.append(sets)

y_index = 0
for sets in points:
    print('row [{0}/{1}]'.format(str(y_index+1), int(res_h)))
    for set in sets:
        ypos = set[0]
        y_index = ypos
        start = set[1]
        end = set[2]
        pyautogui.moveTo(screen_x+start*draw_ratio, screen_y+ypos*draw_ratio)
        pyautogui.dragTo(screen_x+end*draw_ratio, screen_y+ypos*draw_ratio)
