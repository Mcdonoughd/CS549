# Test Dataset Generator
# By Daniel McDonough
# last Updated 10/21/19

import os
from PIL import Image
from os import listdir
from os.path import isfile, join
import random
import math
import cv2

DATASET = "./Dataset/"
MASKS = "./Masks/"
BACKGROUNDS = "./Backgrounds/"
TESTINGMASKS = "./GroundTruthMasks/"
OGLABELS = "./Original_Labels/"
Labels = "./Labels/"

# Determine random mask
def random_mask():
    mask_list = [MASKS + f for f in listdir(MASKS) if isfile(join(MASKS, f))]
    if len(mask_list) == 0:
        print("NO MASKS IN THE FOLDER! Terminating...")
        exit(1)
    if len(mask_list) > 1:
        num = random.randrange(len(mask_list) - 1)
    else:
        num = 0
    mask = Image.open(mask_list[num]).convert("RGBA")
    # mask = mask.resize((8000,8000))
    return mask,mask_list[num]

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
    print(scale_factor)
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
        print("Width:"+str(w))
        print("Height:"+str(h))
        print("Width:" + str(j))
        print("Height:" + str(k))
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
    background = Image.new('RGBA', (960, 720),(0,0,0,255))
    background.paste(img, (x, y), mask=img)
    background.save(TESTINGMASKS + fname, "PNG")
    label = TESTINGMASKS + fname
    return label.split("/")[2]

def combineLabels(label,original_label,new_label_filename):
    OGlabel = os.path.join(OGLABELS,original_label)
    newlabel = os.path.join(TESTINGMASKS,label)

    img1 = cv2.imread(OGlabel)

    # print(img1.size)

    img2 = cv2.imread(newlabel)

    # print(img2.size)
    bit_or = cv2.bitwise_or(img2, img1)

    filename = os.path.join(Labels,new_label_filename)

    cv2.imwrite(filename,bit_or)
    print()

def main():
    # check if folders exist
    if not os.path.exists(MASKS) or not os.path.exists(DATASET) or not os.path.exists(BACKGROUNDS):
        os.mkdir(MASKS)
        os.mkdir(DATASET)
        os.mkdir(BACKGROUNDS)

    mask_list = [MASKS+f for f in listdir(MASKS) if isfile(join(MASKS, f))]
    bg_list = [BACKGROUNDS+f for f in listdir(BACKGROUNDS) if isfile(join(BACKGROUNDS, f))]
    bg_list.sort()
    # Check if empty folder
    if len(mask_list) == 0 or len(bg_list) == 0:
        print("NO MASKS or BACKGROUNDS IN THE FOLDER! Terminating...")
        exit(1)

    for bg in bg_list:

        OG_label = bg.split("/")[2][:-4] + "_L.png"
        print(OG_label)


        bg = Image.open(bg).convert("RGBA")
        # bg = bg.resize((8000,8000))

        mask,mask_name = random_mask()  # pick mask

        # image = Image.open(mask).convert("RGBA")
        rmask,angle = random_rotation(mask)  # compute random rotations
        smask, scale_factor = random_scale(rmask)  # compute random scaling
        fmask,k,j = random_flip(smask)  # compute random flips

        filename = namingconvention(mask_name,angle,scale_factor,k,j)
        new_label_filename = filename[:-4] + "_L.png"
        print(new_label_filename)

        x,y = combine(fmask,bg,filename)
        bn = Binarization(fmask)
        label = saveGroundTruth(bn, x, y, filename)
        print(label)
        combineLabels(label,OG_label,new_label_filename)



if __name__ == '__main__':
    main()