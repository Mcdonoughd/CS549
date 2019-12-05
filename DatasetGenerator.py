# Test Dataset Generator
# By Daniel McDonough
# last Updated 10/21/19

import os
from PIL import Image
from os import listdir
from os.path import isfile, join
import random
import math


DATASET = "./Dataset/"
MASKS = "./Masks/"
BACKGROUNDS = "./Backgrounds/"
TESTINGMASKS = "./GroundTruthMasks/"

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


# Determine random translation of the image onto the background
def random_translation(image,background):

    w,h = image.size  # Width & height of image
    j,k = background.size # Width & height of background


    if w>=j or h>=k:
        print("ERROR DUCK LARGER THAN BACKGROUND")
        exit(1)

    maxside = j-w  # difference in sizes
    maxheight = k-h  # difference in sizes
    x = random.randint(0, maxside)
    y = random.randint(0, maxheight)

    return x,y


# Overlay the image onto the Background
def combine(img,background,name):
    x,y = random_translation(img,background)
    background.paste(img, (x, y), img)
    background.save(DATASET+name, "PNG")
    return x, y


# Name the test images Bird[NUMBER]_R[Rotation]_S[SCALE]_M[FLIP_H][FLIP_W]
def namingconvention(mask,angle,scale,k,j):
    filename = mask.split("/")
    filename = filename[-1]
    filename = filename[:-4]
    filename = filename+"_R"+str(angle)
    filename = filename + "_S" + str(scale).replace(".","-")
    filename = filename + "_M" + str(k) + str(j)
    filename = filename + ".png"
    return filename


# Binarize the given image
def Binarization(img):
    ld = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = ld[x, y]
            if a == 255:
                ld[x,y] = (255,255,255,255)
            else:
                ld[x, y] = (0,0,0,255)
    return img

# save the ground truth
def saveGroundTruth(img,x,y,fname):
    background = Image.new('RGBA', (8000, 8000),(0,0,0,255))
    background.paste(img, (x, y), mask=img)
    background.save(TESTINGMASKS + fname, "PNG")


def main():
    # check if folders exist
    if not os.path.exists(MASKS) or not os.path.exists(DATASET) or not os.path.exists(BACKGROUNDS):
        os.mkdir(MASKS)
        os.mkdir(DATASET)
        os.mkdir(BACKGROUNDS)

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
        x,y = combine(fmask,bg,filename)
        bn = Binarization(fmask)
        saveGroundTruth(bn, x, y, filename)


if __name__ == '__main__':
    main()