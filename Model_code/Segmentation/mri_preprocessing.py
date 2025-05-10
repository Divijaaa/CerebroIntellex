import os, glob

path = "C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/Normal _ Stroke Patient Details"

def segragating_types(path):
  mapping_dataset = {}
  for dir in os.listdir(path):
    if 'Normal' in dir:
      if 'Normal' not in mapping_dataset.keys():
        mapping_dataset["Normal"] = []
      mapping_dataset["Normal"].append(dir)

    if 'Haemorrhagic' in dir:
      if 'Haemorrhagic' not in mapping_dataset.keys():
        mapping_dataset["Haemorrhagic"] = []
      mapping_dataset["Haemorrhagic"].append(dir)

    if 'Ischemic' in dir:
      if 'Ischemic' not in mapping_dataset.keys():
        mapping_dataset["Ischemic"] = []
      mapping_dataset["Ischemic"].append(dir)

  return mapping_dataset

mapping_dataset = segragating_types(path)
mapping_dataset
import shutil
def move_files_to_root_folder(old, new, mapping_dataset):

  for key in mapping_dataset.keys():
    for subdir in mapping_dataset[key]:
      try:
        shutil.copytree(f"{old}/{subdir}",f'{new}/{key}/{subdir}')
      except Exception as e:
        print(e)

move_files_to_root_folder(path, "C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/Dataset_MRI_Folder2", mapping_dataset)
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.image import imread
import pathlib

class_names = mapping_dataset.keys()
nimgs = {}
root_path = "C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/Dataset_MRI_Folder2"
for i in class_names:
  jpg_files = glob.glob(f'{root_path}/{i}/**/*.jpg', recursive=True)
  JPG_files = glob.glob(f'{root_path}/{i}/**/*.JPG', recursive=True)
  png_files = glob.glob(f'{root_path}/{i}/**/*.png', recursive=True)
  nimages = len(jpg_files) + len(png_files) + len(JPG_files)
  nimgs[i] = nimages
  # nimages = len(glob.glob(f'{root_path}/{i}/**/*.jpg', recursive=True))

  # nimgs[i] = nimages

print(nimgs)
plt.figure(figsize=(9, 6))
plt.bar(range(len(nimgs)), list(nimgs.values()), align='center')
plt.xticks(range(len(nimgs)), list(nimgs.keys()))
plt.title('Distribution of Dataset')
plt.show()
import numpy as np
import cv2

def enhance_contrast(image_matrix, bins=256):
    image_flattened = image_matrix.flatten()
    image_hist = np.zeros(bins)

    # frequency count of each pixel
    for pix in image_matrix:
        image_hist[pix] += 1

    # cummulative sum
    cum_sum = np.cumsum(image_hist)
    norm = (cum_sum - cum_sum.min()) * 255
    # normalization of the pixel values
    n_ = cum_sum.max() - cum_sum.min()
    uniform_norm = norm / n_
    uniform_norm = uniform_norm.astype('int')

    # flat histogram
    image_eq = uniform_norm[image_flattened]
    # reshaping the flattened matrix to its original shape
    image_eq = np.reshape(a=image_eq, newshape=image_matrix.shape)

    return image_eq
import cv2

def apply_enhancement(img):
  mask = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)[1][:,:,0]
  dst = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
  a_img =enhance_contrast(dst)
  return a_img


def visualize(image_path, class_name, enhancement=False):
  plt.figure(1,figsize=[20, 3])

  # plt.axis('off')
  n = 0
  for i in range(8):
    n += 1
    plt.suptitle(class_name, fontsize=34)
    img = cv2.imread(image_path[i])
    if enhancement:
      img = apply_enhancement(img)
    plt.subplot(1, 8, n)
    plt.imshow(img)

    plt.title(os.path.dirname(image_path[i]).split("/")[-1])
    plt.axis('off')
  return plt

def plot_images(class_names, enhancement=False):
  image_path = []
  for c in range(len(class_names)):
    image_path = glob.glob(f'{root_path}/{class_names[c]}/**/*.jpg', recursive=True)
    # fig = plt.figure()
    # fig.suptitle(class_names[c])
    visualize(image_path, class_names[c], enhancement).show()
plot_images(list(mapping_dataset.keys()))
import cv2
import numpy as np
import glob

root_path = "C:/Users/Divija agrawal/OneDrive/Desktop/major/mri_segmentation/Dataset_MRI_Folder2"

# Include all possible image extensions
image_extensions = ('*.jpg', '*.jpeg', '*.png')

# Collect all images with different extensions
images = []
for ext in image_extensions:
    images.extend(glob.glob(f"{root_path}/**/{ext}", recursive=True))

# Check if images were found
print(f"Total images found: {len(images)}")
print(images[:5])  # Print first 5 image paths for verification

# Function to read and resize an image
def read_resize(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Warning: Could not read {img_path}")
        return None
    return cv2.resize(img, (256, 256))

# Process images and filter out None values
Data = [read_resize(img) for img in images if read_resize(img) is not None]
Data = np.asarray(Data)

# Check the final shape of the dataset
print(f"Final dataset shape: {Data.shape}")
len(images)

target =  []

for img in images:
  if 'Haemorrhagic' in img:
    target.append(0)
  elif 'Ischemic' in img:
    target.append(1)
  elif 'Normal' in img:
    target.append(2)
Data = Data.flatten().reshape(756, 196608)
Data.shape
#Import required modules
from sklearn.decomposition import PCA

pca = PCA(2) # we need 2 principal components.
converted_data = pca.fit_transform(Data)

converted_data.shape
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize = (10,6))
c_map = plt.cm.get_cmap('jet', 10)
plt.scatter(converted_data[:, 0], converted_data[:, 1], s = 15,
            cmap = c_map , c = np.array(target))
plt.colorbar()
plt.xlabel('PC-1') , plt.ylabel('PC-2')
plt.show()
#Import required modules
from sklearn.decomposition import PCA

pca = PCA(3) # we need 3 principal components.
converted_data = pca.fit_transform(Data)

converted_data.shape
fig = plt.figure(figsize=(14,9))
ax = fig.add_subplot(111,
                     projection='3d')

c_dict = {0: "m", 1: "c", 2:"y"}
label = {0: "Haemorrhagic", 1: "Ischemic", 2:"Normal"}
for l in np.unique(target):
 ix=np.where(target==l)
 ax.scatter(converted_data[:, 0][ix],
            converted_data[:, 1][ix],
            converted_data[:, 2][ix],
            c=c_dict[l],
            s=60,
           label=label[l])

ax.set_xlabel("PC1",
              fontsize=12)
ax.set_ylabel("PC2",
              fontsize=12)
ax.set_zlabel("PC3",
              fontsize=12)

ax.view_init(30, 125)
ax.legend()
plt.title("3D PCA plot")
plt.show()
plot_images(list(mapping_dataset.keys()), True) 