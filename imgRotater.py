# -*- coding:utf-8 -*-

import cv2 as cv
import glob
import imutils
import os
from math import sin, cos
import numpy as np

angle = 225

class ImageRotater:
    def __init__(self):
        self.rh = 0
        self.rw = 0
        self.rc = 0   
        self.imagepath = "./before"
        self.txtpath = "./before"
        self.rotatedimgpath = "./after"
        self.rangle = angle * np.pi / 180
            
        self.rot_matrix = np.array([[np.cos(self.rangle), -np.sin(self.rangle)], [np.sin(self.rangle), np.cos(self.rangle)]])

    def rotatebbox(self, tmp):
        for i in range(len(tmp)):
            tmp[i] = int(tmp[i])

        new_bbox = []

        if len(tmp) > 1:
            upper_left_corner_shift = (tmp[0] - self.w / 2, -self.h / 2 + tmp[1])
            upper_right_corner_shift = (tmp[2] - self.w / 2, -self.h / 2 + tmp[1])
            lower_left_corner_shift = (tmp[0] - self.w / 2, -self.h / 2 + tmp[3])
            lower_right_corner_shift = (tmp[2] - self.w / 2, -self.h / 2 + tmp[3])

            new_lower_right_corner = [-1, -1]

            new_upper_left_corner = []

            for i in (upper_left_corner_shift, upper_right_corner_shift, lower_left_corner_shift, lower_right_corner_shift):
                new_coords = np.matmul(self.rot_matrix, np.array((i[0], -i[1])))
                x_prime, y_prime = self.rw / 2 + new_coords[0], self.rh / 2 - new_coords[1]

                if new_lower_right_corner[0] < x_prime:
                    new_lower_right_corner[0] = x_prime

                if new_lower_right_corner[1] < y_prime:
                    new_lower_right_corner[1] = y_prime

                if len(new_upper_left_corner) > 0:
                    if new_upper_left_corner[0] > x_prime:
                        new_upper_left_corner[0] = x_prime

                    if new_upper_left_corner[1] > y_prime:
                        new_upper_left_corner[1] = y_prime
                else:
                    new_upper_left_corner.append(x_prime)
                    new_upper_left_corner.append(y_prime)

            tmp = [new_upper_left_corner[0], new_upper_left_corner[1], new_lower_right_corner[0], new_lower_right_corner[1]]

            for i in range(len(tmp)):
                tmp[i] = str(round(tmp[i]))

        return tmp

    def make_folder(self):
        if not os.path.isdir(self.rotatedimgpath):
            os.mkdir(self.rotatedimgpath)
        self.savefolder= os.path.join(self.rotatedimgpath, str(angle))  
        if not os.path.isdir(self.savefolder):
            os.mkdir(self.savefolder)

    # def rotate90(self, tmp):
    #     tmp[0], tmp[1]= tmp[1], tmp[0]
    #     tmp[2], tmp[3]= tmp[3], tmp[2]
    #     tmp[1]= str(self.rh-int(tmp[1]))
    #     tmp[3]= str(self.rh-int(tmp[3]))
    #     tmp[1], tmp[3] = tmp[3], tmp[1]
    #     return tmp

    # def rotate180(self, tmp):
    #     tmp[0]= str(self.rw-int(tmp[0]))
    #     tmp[2]= str(self.rw-int(tmp[2]))
    #     tmp[1]= str(self.rh-int(tmp[1]))
    #     tmp[3]= str(self.rh-int(tmp[3]))
    #     tmp[0], tmp[1], tmp[2], tmp[3]= tmp[2], tmp[3], tmp[0], tmp[1]
    #     return tmp

    def get_img_txt(self):
        self.imageList= glob.glob(os.path.join(self.imagepath, '*.JPG'))
        self.txtList= glob.glob(os.path.join(self.txtpath, '*.txt'))

    def imageRotate(self):
        self.get_img_txt()
        self.make_folder()
        for img, txt in zip(self.imageList, self.txtList):
            self.imagename = os.path.split(img)[-1].split('.')[0]
            image = cv.imread(os.path.join(img))
            rotated = imutils.rotate_bound(image, -angle)
            self.h, self.w, self.c = image.shape
            self.rh, self.rw, self.rc = rotated.shape
            imagepath = os.path.join(self.savefolder, self.imagename+".jpg")
            cv.imwrite(imagepath, rotated)
            self.update_txt(txt)

    def update_txt(self, txt):
        f = open(txt, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            tmp = line.strip("\n").split(" ")
            if len(tmp) > 3:
                tmp = self.rotatebbox(tmp)
                # if angle == 90:
                #     tmp = self.rotate90(tmp)
                # elif angle == 180:
                #     tmp = self.rotate180(tmp)
            lines[lines.index(line)] = ' '.join(tmp)
        lines = '\n'.join(lines)
        f = open(os.path.join(self.savefolder, self.imagename+".txt"), "w")
        f.write(lines)
        f.close


if __name__ == "__main__":
    img = ImageRotater()
    img.imageRotate()
