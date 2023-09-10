import numpy as np 
import cv2 as cv

p1 = np.zeros((400,400,3),dtype=np.uint8)
p1[:,:]=(1,150,100)
p1_split = p1[:,:,1]
print(np.shape(p1),np.shape(p1_split))
cv.waitKey(0)
cv.destroyAllWindows()
