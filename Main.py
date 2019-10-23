# Test Dataset Generator
# By Daniel McDonough
# last Updated 10/21/19

import cv2
import os
import numpy as np
from PIL import Image
from os import listdir
from os.path import isfile, join
import random
import math

DATASET = "./Dataset/"
MASKS = "./Masks/"
BACKGROUNDS = "./Backgrounds/"
TESTINGMASKS = "./OverlayedMasks/"

# Determine random Background
def random_background():
    background_list = [BACKGROUNDS + f for f in listdir(BACKGROUNDS) if isfile(join(BACKGROUNDS, f))]
    if len(background_list) == 0:
        print("NO MASKS IN THE FOLDER! Terminating...")
        exit(1)
    if len(background_list) > 1:
        num = random.randrange(len(background_list) - 1)
    else:
        num = 0

    background = Image.open(background_list[num]).convert("RGBA")
    background = background.resize((8000,8000))

    return background

# rotate image
def random_rotation(image):
    angle = random.randrange(0,360)
    rotatedimage = image.rotate(angle, expand=True)
    return rotatedimage, angle

# scale image
def random_scale(image):
    w,h = image.size
    scale_factor = random.randrange(10, 40)/20

    image = image.resize((math.ceil(w*scale_factor),math.ceil(h*scale_factor)))
    return image, scale_factor


# Mirror image
def random_flip(image):
    k = random.randint(0, 1)
    if k:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    j = random.randint(0, 1)
    if j:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return image,k,j

# determine random translation of the image onto the background
def random_translation(image,background):

    w,h = image.size  # Width & height of image
    j,k = background.size # Width & height of background
    print(image.size)
    print(background.size)

    if w>=j or h>=k:
        print("ERROR MASK LARGER THAN BACKGROUND")
        exit(1)

    maxside = j-w  # difference in sizes
    maxheight = k-h  # difference in sizes
    x = random.randint(0, maxside)
    y = random.randint(0, maxheight)

    return x,y


# overlay the image onto the Background
def combine(img,background,name):
    x,y = random_translation(img,background)
    background.paste(img, (x, y), img)
    background.save(DATASET+name, "PNG")

def namingconvention(mask,angle,scale,k,j):
    filename = mask.split("/")
    filename = filename[-1]
    filename = filename[:-4]
    filename = filename+"_R"+str(angle)
    filename = filename + "_S" + str(scale)
    filename = filename + "_M" + str(k) + str(j)
    filename = filename + ".png"
    return filename

# TODO make more bird crops

def saveknown(img,filename):
    img.save(TESTINGMASKS + filename, "PNG")


def main():
    # check if folders exist
    if not os.path.exists(MASKS) or not os.path.exists(DATASET) or not os.path.exists(BACKGROUNDS):
        print("Folders may not exist! Terminating...")
        exit(1)

    mask_list = [MASKS+f for f in listdir(MASKS) if isfile(join(MASKS, f))]

    # Check if empty folder
    if len(mask_list) == 0:
        print("NO MASKS IN THE FOLDER! Terminating...")
        exit(1)

    for mask in mask_list:
        image = Image.open(mask).convert("RGBA")
        rmask,angle = random_rotation(image)  # compute random rotations
        smask, scale_factor = random_scale(rmask)  # compute random scaling
        fmask,k,j = random_flip(smask)  # compute random flips
        bg = random_background()  # pick background
        filename = namingconvention(mask,angle,scale_factor,k,j)
        saveknown(fmask,filename)
        combine(fmask,bg,filename)


if __name__ == '__main__':
    main()