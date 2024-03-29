# -*- coding: utf-8 -*-
"""Image Segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DzIY10c5KKaDGhdkjl3FhmvhCSi_Nddn

จำลองไดร์ฟของ google drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""นำเข้าไลบราลี่ที่จำเป็น"""

# Commented out IPython magic to ensure Python compatibility.
from skimage.color import rgb2gray
import numpy as np
import cv2
import matplotlib.pyplot as plt
# %matplotlib inline
from scipy import ndimage

"""ตั้งค่าพาร์ทของรูปภาพ"""

impath = "/content/drive/My Drive/ku-csc/Digital Image Processing/Project/chair2.jpg"

"""**Region-based Segmentation**

นำเข้ารูปและพล็อต
"""

image = plt.imread(impath)
image.shape
plt.title("Input Image")
plt.imshow(image)

"""เปลี่ยนเป็น grayscale"""

gray = rgb2gray(image)
plt.title("Gray-Scale of input image")
plt.imshow(gray, cmap='gray')

"""ทำ global threshold"""

gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
for i in range(gray_r.shape[0]):
    if gray_r[i] > gray_r.mean():
        gray_r[i] = 1
    else:
        gray_r[i] = 0
gray = gray_r.reshape(gray.shape[0],gray.shape[1])
plt.title("Global Threshold")
plt.imshow(gray, cmap='gray')

"""ทำ locale threshold"""

gray = rgb2gray(image)
gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
for i in range(gray_r.shape[0]):
    if gray_r[i] > gray_r.mean():
        gray_r[i] = 3
    elif gray_r[i] > 0.5:
        gray_r[i] = 2
    elif gray_r[i] > 0.25:
        gray_r[i] = 1
    else:
        gray_r[i] = 0
gray = gray_r.reshape(gray.shape[0],gray.shape[1])
plt.title("Locale Threshold")
plt.imshow(gray, cmap='gray')

"""**Edge Detection Segmentation**"""

image = plt.imread(impath)
plt.title("Input image")
plt.imshow(image)

"""**Sobel Operation**"""

# converting to grayscale
gray = rgb2gray(image)

# defining the sobel filters
sobel_horizontal = np.array([np.array([1, 2, 1]), np.array([0, 0, 0]), np.array([-1, -2, -1])])
print(sobel_horizontal, '\nThis is a kernel for detecting horizontal edges\n')
 
sobel_vertical = np.array([np.array([-1, 0, 1]), np.array([-2, 0, 2]), np.array([-1, 0, 1])])
print(sobel_vertical, '\nThis is a kernel for detecting vertical edges\n')

out_h = ndimage.convolve(gray, sobel_horizontal, mode='reflect')
out_v = ndimage.convolve(gray, sobel_vertical, mode='reflect')
# here mode determines how the input array is extended when the filter overlaps a border.

plt.imshow(out_h, cmap='gray')
plt.title("Result of sobel horizontal")

plt.imshow(out_v, cmap='gray')
plt.title("Result of sobel virtical")

"""**Lapacian Operation**"""

kernel_laplace = np.array([np.array([1, 1, 1]), np.array([1, -8, 1]), np.array([1, 1, 1])])
print(kernel_laplace, '\nThis is a laplacian kernel\n')

out_l = ndimage.convolve(gray, kernel_laplace, mode='reflect')
plt.imshow(out_l, cmap='gray')
plt.title("The result of lapacian operation")

"""**Image Segmentation based on Clustering(K-MEAN)**

using scikitlearn module
"""

pic = plt.imread(impath)/255  # dividing by 255 to bring the pixel values between 0 and 1
print(pic.shape)
plt.imshow(pic)
plt.title("Input Image")

pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
pic_n.shape

from sklearn.cluster import KMeans
kval = 3
kmeans = KMeans(n_clusters=kval, random_state=0).fit(pic_n)
pic2show = kmeans.cluster_centers_[kmeans.labels_]

cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
plt.imshow(cluster_pic)
plt.title('Segmented Image when K = %i' % kval)

"""**K-Mean Clustering**

using opencv module
"""

original_image = cv2.imread(impath)

img=cv2.cvtColor(original_image,cv2.COLOR_BGR2RGB)

vectorized = np.float32(img.reshape((-1,3)))

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

K = 5
attempts=10
ret,label,center=cv2.kmeans(vectorized,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)

center = np.uint8(center)

res = center[label.flatten()]
result_image = res.reshape((img.shape))

figure_size = 15
plt.figure(figsize=(figure_size,figure_size))
plt.subplot(1,2,1),plt.imshow(img)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1,2,2),plt.imshow(result_image)
plt.title('Segmented Image when K = %i' % K), plt.xticks([]), plt.yticks([])
plt.show()