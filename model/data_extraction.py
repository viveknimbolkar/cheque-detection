import os
import cv2
# from google.colab.patches import cv2_imshow
import easyocr
# from matplotlib import pyplot as plt
# import numpy as np


class DataExtraction:

    def __init__(self,obj):
        image = cv2.imread(obj)
        di = {'Date': [65, 100, 850, 1100],
              'Amount_num': [190, 250, 870, 1090],
              'Amount_str': [160, 210, 235, 1600],
              'Pay': [110, 180, 160, 830],
              'Sign': [280, 370, 850, 1100],
              'Acc_no': [250, 320, 190, 500],
              'IFSC': [0, 130, 410, 700],
              'Codes': [430, 500, 300, 900]
              }

        final = {}
        for val in di:
            x, w, y, h = di[val]
            c_i = image[x:w, y:h]
            final[val] = c_i

        self.date = self.Date(final["Date"])
        self.amount_num = self.Other(final["Amount_num"])
        self.amount_str = self.Other(final["Amount_str"])
        self.pay = self.Other(final["Pay"])
        self.acc_no = self.Other(final["Acc_no"])
        self.IFSC = self.IFSC(final["IFSC"])

    def getDetails(self):
        return [self.pay,self.acc_no,self.amount_str,self.amount_num,self.IFSC,self.date]

    def Date(self, obj):
        IMAGE_PATH = obj

        image = IMAGE_PATH
        result = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (255, 255, 255), 5)

        # cv2_imshow(thresh)
        # cv2_imshow(result)
        # cv2.imwrite('result.png', result)

        reader = easyocr.Reader(['en'])
        result = reader.readtext(thresh)
        val = result[0][1]
        val = ''.join(val.split(' '))
        date = val[:2] + '-' + val[2:4] + '-' + val[4:]
        return date

    def IFSC(self, obj):
        IMAGE_PATH = obj

        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        val = result[4][1]
        return val

    def Other(self, obj):
        IMAGE_PATH = obj

        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        val = result[0][1]
        return val


if __name__ == '__main__':
    out = DataExtraction()
