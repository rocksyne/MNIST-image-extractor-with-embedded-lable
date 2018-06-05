"""
MIT License

Copyright (c) 2018 Agyeman Rockson [rocksyne@gmail.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


CREDIT: [ceykmc/mnist.py] https://gist.github.com/ceykmc/c6f3d27bb0b406e91c27

CAUTION: 
---------------------------------------------------------------------------------
This piece of code was implemented isn a "shabby" manner to complete an adhoc 
projetc and is being shared with the hope that it saves some one some work. You
are free to clean it up and give major credit to the original author (ceykmc)


DOCUMENT
----------------------------------------------------------------------------------
This piece of code is an addition to the work done by ceykmc. This code is supposed
to extract png images from the mnist compressed dataset and embed their labels into 
the file name to make it relevant to anyone who wants to use it in a different way
as they please.

EXAMPLE: using test dataset
    Pattern: OLDFILENAME.LABLE.FILE_EXTENSION
    old file name: 9564.png
    lable: 8
    new file name: 9564.8.png

USAGE:
    1. Go to http://yann.lecun.com/exdb/mnist/
    
    2. Download the tarin and test compressed mnist files
    
    You should have something like this:
    train-images-idx3-ubyte.gz:  training set images (9912422 bytes)
    train-labels-idx1-ubyte.gz:  training set labels (28881 bytes)
    t10k-images-idx3-ubyte.gz:   test set images (1648877 bytes)
    t10k-labels-idx1-ubyte.gz:   test set labels (4542 bytes) 
    
    3. Rn the following methods in the sequence the occur
    eg:
        This is example for the train images
        ------------------------------------------------------
        extract_labels("./train-labels.idx1-ubyte","t_label")
        extract_images("./train-images.idx3-ubyte","./img/")
        embed_lable_into_image("t_label","./img/")
        
    4. Do the same for the test dataset as well
    
"""


import numpy as np
import cv2
import struct
import os

# Code by [ceykmc/mnist.py] https://gist.github.com/ceykmc/c6f3d27bb0b406e91c27
def extract_labels(mnist_label_file_path, label_file_path):
    with open(mnist_label_file_path, "rb") as mnist_label_file:
        # 32 bit integer magic number
        mnist_label_file.read(4)
        # 32 bit integer number of items
        mnist_label_file.read(4)
        # actual test label
        label_file = open(label_file_path, "w")
        label = mnist_label_file.read(1)
        while label:
            label_file.writelines(str(label[0]) + "\n")
            label = mnist_label_file.read(1)
        label_file.close()


# Code by [ceykmc/mnist.py] https://gist.github.com/ceykmc/c6f3d27bb0b406e91c27       
def extract_images(images_file_path, images_save_folder):
    # images_file_path = "./t10k-images-idx3-ubyte"
    with open(images_file_path, "rb") as images_file:
        # 32 bit integer magic number
        images_file.read(4)
        # 32 bit integer number of images
        images_file.read(4)
        # 32 bit number of rows
        images_file.read(4)
        # 32 bit number of columns
        images_file.read(4)
        # every image contain 28 x 28 = 784 byte, so read 784 bytes each time
        count = 1
        image = np.zeros((28, 28, 1), np.uint8)
        image_bytes = images_file.read(784)
        while image_bytes:
            image_unsigned_char = struct.unpack("=784B", image_bytes)
            for i in range(784):
                image.itemset(i, image_unsigned_char[i])
            image_save_path = "./%s/%d.png" % (images_save_folder, count)
            cv2.imwrite(image_save_path, image)
            image_bytes = images_file.read(784)
            count += 1
            
            
# code by [me; rocksyne ] https://github.com/rocksyne?tab=repositories
# This code needs cleaning up. Please help if you can.           
def embed_lable_into_image(label_file_path,images_save_folder):
    file = open(label_file_path,"r") 
    imageP = os.path.join(os.getcwd(),images_save_folder)

    lableArray = []

    for line in file:
        lableArray.append(int(line))

    for x in os.listdir(imageP):
        originalImageFullPath = os.path.join(imageP,x)
        fileSplit = x.split(".")
        fileName = fileSplit[0]
        fileExt = "."+str(fileSplit[1])
        newName = str(fileName)+"."+str(lableArray[int(fileName)-1])+fileExt

        newImageFullPath = os.path.join(imageP,newName)
        os.rename(originalImageFullPath,newImageFullPath)

    print("done!")
