import os
import cv2
import easyocr


class DataExtraction:

    def __init__(self,obj):
        image = cv2.imread(obj)
        di = {
              'Date': [0, 100, 1300, 1900],
              'Amount_num': [250, 400, 1440, 1800],
              'Amount_str': [210, 300, 280, 1800],
              'Pay': [150, 220, 130, 1350],
              'Signature': [400, 640, 1200, 1800],
              'Acc_no': [400, 500, 160, 750],
              'IFSC': [0, 150, 600, 1100],
              'Codes': [700, 800, 300, 1400]
            }

        self.final = {}
        for val in di:
            x, w, y, h = di[val]
            c_i = image[x:w, y:h]
            self.final[val] = c_i

        self.date = self.Date(self.final["Date"])
        self.amount_num = self.Amount_num(self.final["Amount_num"])
        self.amount_str = self.Other(self.final["Amount_str"])
        self.pay = self.Other(self.final["Pay"])
        self.acc_no = self.Other(self.final["Acc_no"])
        self.IFSC = self.IFSC(self.final["IFSC"])


    def getDetails(self):
        return [self.pay,self.acc_no,self.amount_str,self.amount_num,self.IFSC,self.date,self.final['Signature']]

    def Amount_num(self,obj):
        IMAGE_PATH = obj
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        val = result[0][1]
        temp = ''
        li = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for v in val:
            if v in li:
                temp += v
        return temp


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
        result = reader.readtext(IMAGE_PATH)[-1][1].split(' ')[-1]
        return result

    def Other(self, obj):
        IMAGE_PATH = obj
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        val = result[0][1]
        return val


if __name__ == '__main__':
    out = DataExtraction()
