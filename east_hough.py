import cv2
import numpy as np
import skimage 
from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny

import os
from dotenv import load_dotenv

load_dotenv()

EAST_MODEL_PATH = os.getenv('EAST_MODEL_PATH')

def east_detect(image_path,  args):    
    image = cv2.imread(image_path)
    
    args = {
            "image":image_path,
            "east": EAST_MODEL_path,
            "min_confidence": 0.5,
            "margin_tollerance":9,
            "width": 1280,
            "height": 1280
        }
    if(args["east"] is None):
        print('Não foi possível reconhecer variável ambiente.')
        print('ENV VAR: ', args["east"])
        exit() 
    
    (H, W) = image.shape[:2]
    (newW, newH) = (args["width"], args["height"])
    rW = W / float(newW)
    rH = H / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    net = cv2.dnn.readNet(args["east"])
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (numRows, numCols) = scores.shape[2:4]
    angl = []
    for y in range(0, numRows):
        
        scoresData = scores[0, 0, y]
        anglesData = geometry[0, 4, y]
        for x in range(0, numCols):
            if scoresData[x] < args["min_confidence"]:
                continue
            
            angle = anglesData[x]
            angl.append(angle*180/(np.pi))
    return np.median(angl)
    
    
def east(image_path,args):
        angle = east_detect(image_path, args)
        return angle
    
    
    
def hough_transforms(image):
	        
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.GaussianBlur(gray,(11,11),0)
    edges = canny(thresh)
    tested_angles = np.deg2rad(np.arange(0.1, 180.0))
    h, theta, d = hough_line(edges, theta=tested_angles)
    accum, angles, dists = hough_line_peaks(h, theta, d)

    return accum, angles, dists


def east_hough_line(image, args):
    image, angle = east(image, args)
    h, theta, d = hough_transforms(image)
    theta = np.rad2deg(np.pi/2-theta)
    #theta = np.rad2deg(theta-np.pi/2)
    margin = args['margin_tollerance']
    low_thresh = angle-margin
    high_thresh = angle+margin
    filter_theta = theta[theta>low_thresh]
    filter_theta = filter_theta[filter_theta < high_thresh]
    
    return image, np.median(filter_theta)

