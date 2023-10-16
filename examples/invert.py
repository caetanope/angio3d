import cv2
import sys
import glob

imagesFolder = sys.argv[1] + '*.png'
destination = sys.argv[2]
print(imagesFolder)
imagesPath = glob.glob(imagesFolder)
print(imagesPath)
for imagePath in imagesPath:
    image = cv2.imread(imagePath)
    image = 255 - image
    name = imagePath.split('\\')[-1]
    print(destination + name)
    cv2.imwrite(destination + name,image)
    