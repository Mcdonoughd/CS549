# Mean Average Precision (mAP)
# By Daniel McDonough (12/6/19)

import cv2
import os
from os import listdir
from os.path import isfile, join
from statistics import mean
import numpy as np

GROUNDTRUTHMASKS = "./GroundTruthMasks/"
PREDICTEDMASKS = "./PredictedMasks/"


# Caluculate the Intersection over the UNION
# TODO
def IOU(Predicted,Truth):

    Added = Predicted + Truth
    Intersection = np.where(Added > 255)
    Union = np.where(Added > 0)

    iou  = len(Intersection)/len(Union)

    # Uncomment if you want to see the image version of the Intersection and union of masks
    # Intersection = Added.copy()
    # Intersection[np.where(Added == 255)] = 0
    # Intersection[np.where(Added > 255)] = 255
    #
    # Union = Added.copy()
    # Union[np.where(Added > 255)] = 255
    #
    #
    # imS = cv2.resize(Intersection, (960, 540))  # Resize image
    # cv2.imshow("output", imS)  # Show image
    # imP = cv2.resize(Union, (960, 540))  # Resize image
    # cv2.imshow("Union", imP)  # Show image
    # cv2.waitKey(0)
    # print("")

    return iou


def main():
    # check if folders exist
    if not os.path.exists(GROUNDTRUTHMASKS) or not os.path.exists(PREDICTEDMASKS):
        os.mkdir(GROUNDTRUTHMASKS)
        os.mkdir(PREDICTEDMASKS)

    Truth_list = [f for f in listdir(GROUNDTRUTHMASKS) if isfile(join(GROUNDTRUTHMASKS, f))]
    Predicted_list = [f for f in listdir(PREDICTEDMASKS) if isfile(join(PREDICTEDMASKS, f))]

        # Check if empty folder
    if len(Truth_list) == 0 or len(Predicted_list) == 0:
        print("NO MASKS IN THE FOLDER! Terminating...")
        exit(1)


    IOU_List = []
    for t in Truth_list:
        filename_list = t.split("_")
        filetested = filename_list[0]
        if os.path.isfile(PREDICTEDMASKS+filetested+".png"):
            Predicted = cv2.imread(PREDICTEDMASKS+filetested+".png")

            Truth = cv2.imread(GROUNDTRUTHMASKS+t)
            iou = IOU(Predicted,Truth)

            IOU_List.append(iou)
            print("Accuracy for test " + t + ": " + str(iou))

    mAP = mean(IOU_List)
    print("The mean accuracy percentage: " + str(mAP))



if __name__ == '__main__':
    main()
