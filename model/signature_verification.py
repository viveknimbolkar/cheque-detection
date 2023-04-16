import cv2

class MyImage:
    def __init__(self, img_name, optional=0):
        self.img = img_name
        self.__name = img_name

    def __str__(self):
        return self.__name


class VerifySignature:
    def __init__(self, obj1, obj2):
        self.img1 = MyImage(obj1, 0)  # queryImage
        self.img2 = MyImage(obj2, 0)  # trainImage

    def find(self):

        self.img1.img = cv2.cvtColor(self.img1.img, cv2.COLOR_BGR2GRAY)
        self.img2.img = cv2.cvtColor(self.img2.img, cv2.COLOR_BGR2GRAY)

        # =============================================================
        # figure, ax = plt.subplots(1, 2, figsize=(16, 8))
        #
        # ax[0].imshow(img1.img, cmap='gray')
        # ax[1].imshow(img2.img, cmap='gray')
        # ==================================================================

        # Initiate SIFT detector
        sift = cv2.xfeatures2d.SIFT_create()

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.img1.img, None)
        kp2, des2 = sift.detectAndCompute(self.img2.img, None)

        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []
        good_without_list = []
        for m, n in matches:
            if m.distance < 0.65 * n.distance:
                good.append([m])
                good_without_list.append(m)

        if len(good) >= 8:
            return True
        else:
            return False
