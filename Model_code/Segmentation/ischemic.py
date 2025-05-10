import cv2
import numpy as np
from matplotlib import pyplot as plt
img1 = cv2.imread("C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/Dataset_MRI_Folder2/Ischemic/Amina_Stroke_Ischemic/DWI/Amina DWI-16.jpg")
plt.imshow(img1)
plt.axis("off")
mask = cv2.threshold(img1, 250, 255, cv2.THRESH_BINARY)[1][:,:,0]
dst = cv2.inpaint(img1, mask, 7, cv2.INPAINT_NS)
# dst = cv2.bitwise_not(dst)
plt.imshow(dst)
from PIL import Image, ImageFilter


im1 = Image.fromarray(dst)
im1 = im1.filter(ImageFilter.MedianFilter(size = 3))
plt.imshow(im1)
ax = plt.subplots(1, 2)[1]
# plt.imshow(cv2.GaussianBlur(img_errode, (1, 1), 0))
img_bright = cv2.convertScaleAbs(np.asarray(im1), alpha=1.5, beta=10)
ax[0].imshow(img_bright)

kernel = np.ones((1, 1), np.uint8)
img_errode = cv2.erode(img_bright, kernel)

ax[1].imshow(img_errode)
def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

gamma = 0.1 
adjusted = adjust_gamma(img_errode, gamma=gamma)
plt.imshow(adjusted)                               # change the value here to get different result
adjusted_path = "C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/models/adjusted_ischemic.png"
cv2.imwrite(adjusted_path, adjusted)
fig, ax = plt.subplots(1, 2)

ax[0].imshow(img1)
ax[0].set_title("Original Image")

ax[1].imshow(adjusted)
ax[1].set_title("Segmented Ischemic Stroke")
plt.show()