from skimage.metrics import structural_similarity as ssim
from urllib.request import urlopen
import urllib.request

import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob

class compareImages:
    def __init__(self,url,urls,rate):
        self.url=url
        self.urls=urls
        self.rate=rate
        original=self.getImages(self.url)
        self.dit=self.comparision(original,self.urls,self.rate)

    def showDetails(self):
        for i in self.dit:
            print("Image Location="+str(self.dit[i][2])+" Similarity=" +str(self.dit[i][1]))


    def showImages(self):

        for i in self.dit:


            fig = plt.figure(self.dit[i][2])

            ax = fig.add_subplot(1, 2, 1)

            plt.suptitle(" SIMILARITY: %.2f %%" % (self.dit[i][1]*100))
            plt.imshow(self.dit[i][0], cmap=plt.cm.gray)
            plt.axis('off')

        plt.show()




    def comparision(self,original,urls,rate):
        dit={}
        i=1
        for f in urls:
            comparision_image = self.getImages(f)
            title = f;

            x = 0
            y = 0
            if (original.shape[0] <= comparision_image.shape[0]):
                x = original.shape[0]
            else:
                x = comparision_image.shape[0]
            if (original.shape[1] <= comparision_image.shape[1]):
                y = original.shape[1]
            else:
                y = comparision_image.shape[1]

            original = cv2.resize(original, (x, y))
            comparision_image = cv2.resize(comparision_image, (x, y))
            d=self.compare_images(original, comparision_image, title,rate)
            if d is not None:
                dit[i]=d
                i=i+1

        return dit



    def getImages(self,url):
        req = urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype="uint8")
        image = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        return image
        #cv2.imshow(url, image)
        #cv2.waitKey(0)

    def mse(self,imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def compare_images(self,imageA, imageB, title,rate):
       # m = self.mse(imageA, imageB)
        s = ssim(imageA, imageB)
        if(s>=(rate/100)):
        # setup the figure
            fig = plt.figure(title)
            plt.suptitle(" SIMILARITY: %.2f" % ( s))
            return [imageB,s,title]
            #ax = fig.add_subplot(1, 2, 1); plt.imshow(imageA, cmap=plt.cm.gray); plt.axis("off"); ax = fig.add_subplot(1, 2, 2); plt.imshow(imageB, cmap=plt.cm.gray); plt.axis("off"); plt.show()

ls=["https://images.unsplash.com/photo-1475855581690-80accde3ae2b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
    "https://images.unsplash.com/photo-1510798831971-661eb04b3739?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",


    ]
similarity_rate=25
orig_image="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60"
obj=compareImages(orig_image,ls,similarity_rate)
obj.showImages()
obj.showDetails()