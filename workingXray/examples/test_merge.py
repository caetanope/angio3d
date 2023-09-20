import cv2
import numpy as np


def addValues(A,B):
    Al = int(A)
    Bl = int(B)
    if Al + Bl > 255:
        return 255
    return A + B
    

def addImages(A, B):
    if len(A.shape) > 1:
        result = list(map(addImages, A, B))
    else:
        result = list(map(addValues, A, B))
    result = np.asarray(result, dtype=np.uint8)
    return result


ribs = cv2.imread("ribs.jpg")
heart = cv2.imread("heart.jpg")

heart = 255-heart

heartHeight = heart.shape[0]
heartWidth = heart.shape[1]
#print(heart.shape)
#print(ribs.shape)

ribs = cv2.resize(ribs, [ribs.shape[1]*2,ribs.shape[0]*2])

croppedRibs = ribs[ribs.shape[1]-heartHeight:ribs.shape[1], ribs.shape[0]-heartWidth:ribs.shape[0]]



print(croppedRibs.shape)
result = addImages(heart, croppedRibs)
print(result.shape)

#result = 255 - result

cv2.imshow("ribs", result)

h, w, _ = result.shape
result2 = np.zeros((h,w,1),np.uint8)
h_mask, w_mask  = (5, 5)
threshold = 200
for j in range(h):
    for i in range(w):
        if result[j,i,0] > threshold:
            ymin = (j - h_mask) if (j - h_mask) >= 0 else 0
            ymax = (j + h_mask) if (j + h_mask) < h else (h - 1)
            xmin = (i - w_mask) if (j - w_mask) >= 0 else 0
            xmax = (i + w_mask) if (j + w_mask) < w else (w - 1)
            result2[j,i] = cv2.mean(result[ymin:ymax,xmin:xmax,0])[0]
        else:
            result2[j,i] = result[j,i,0]

cv2.imshow("ribs2", result2)

cv2.waitKey()