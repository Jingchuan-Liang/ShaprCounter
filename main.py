import numpy as np 
import cv2 as cv
import math as maths

def G_Contrast_Param(G_CParam):
    print( "G_contrast: %d" %(G_CParam))

def G_Binary_Param(G_BiParam):
    print("G_threshold: %d" %G_BiParam)

def B_Contrast_Param(B_CParam):
    print( "B_contrast: %d" %(B_CParam))

def B_Binary_Param(B_BiParam):
    print("B_threshold: %d" %(B_BiParam))

def G_lightness_Param(G_LtParam):
    print("G_lightness: %d" %(G_LtParam-200))
    
def B_lightness_Param(B_LtParam):
    print("B_lightness: %d" %(B_LtParam-200))

def UI_Deploy():
    cv.namedWindow("Source Image",cv.WINDOW_AUTOSIZE)
    cv.namedWindow("Channel_Green_ROI", cv.WINDOW_AUTOSIZE)
    cv.namedWindow("Channel_Blue_ROI", cv.WINDOW_AUTOSIZE)

    cv.createTrackbar("G_Lightness","Channel_Green_ROI",50,400,G_lightness_Param)
    cv.createTrackbar("G_contrast","Channel_Green_ROI",50,100,G_Contrast_Param) 
    cv.createTrackbar("G_Threshold","Channel_Green_ROI",200,300,G_Binary_Param)
    #the callback function designated at will take the value of the slider as the pass-on param
    cv.createTrackbar("B_Lightness", "Channel_Blue_ROI",170,400,B_lightness_Param)
    cv.createTrackbar("B_contrast","Channel_Blue_ROI",50,100,B_Contrast_Param) 
    cv.createTrackbar("B_Threshold","Channel_Blue_ROI",200,300,B_Binary_Param)
    #lightness adjustment: use margin quantity to simulate darken 



def img_adjustment():
    UI_Deploy()
    src = cv.imread("D:/cv_tests/dataset1.jpg") #need to have the format subflix
    cv.imshow("Source Image",src) #gennerated window title with image selected   
    h,w,c = src.shape
    H_roi_Prct_low =0.1
    H_roi_Prct_up =0.9
    W_roi_Prct_low =0.1
    W_roi_Prct_up =0.9
    h1 = maths.floor(H_roi_Prct_up*h)
    h0 = maths.floor(H_roi_Prct_low*h)
    w1 = maths.floor(W_roi_Prct_up*w)
    w0 = maths.floor(W_roi_Prct_low*w)
    ROI = np.zeros((h1-h0,w1-w0,3)) #so we define 3-channel ROI here 
    B_base = np.zeros_like(ROI[:,:,1])
    G_base = np.zeros_like(ROI[:,:,1])

    while True:
        ROI = src[h0:h1,w0:w1,:]
        print("ROI_shape is",np.shape(ROI))
        G_ROI = ROI[:,:,1]
        B_ROI = ROI[:,:,0]
        Bpos_lightns = cv.getTrackbarPos("B_Lightness","Channel_Blue_ROI") #define gamma
        Bpos_contrast = cv.getTrackbarPos("B_contrast","Channel_Blue_ROI")/100
        Bpos_thersh = cv.getTrackbarPos("B_Threshold","Channel_Blue_ROI")

        Gpos_lightns = cv.getTrackbarPos("G_Lightness","Channel_Green_ROI") #define gamma
        Gpos_contrast = cv.getTrackbarPos("G_contrast","Channel_Green_ROI")/100
        Gpos_thersh = cv.getTrackbarPos("G_Threshold","Channel_Green_ROI")

        #print(Bpos_contrast)
        """print to check shapes to see if operation is applicable"""
        #print("G_ROI_shape is",np.shape(G_ROI))
        #print("B_ROI_shape is",np.shape(B_ROI))
        #print("B_base shape is", np.shape(B_base))
        #print("B_CrstAdd_shape is",np.shape(B_CrstAdd))
        B_imgajst = cv.addWeighted(B_ROI, Bpos_contrast, B_base, 0.5, Bpos_lightns, dtype = cv.CV_8UC1) #datatype normalisation
        G_imgajst = cv.addWeighted(G_ROI, Gpos_contrast, G_base, 0.5, Gpos_lightns, dtype = cv.CV_8UC1)
        '''supported datatype in opencv to represent an image includes integar[0,255] and float[0,1], 
        having different value domains hence would cause image arithmetic problems'''
        #print(B_imgajst)
        ret1, B_BiThresh = cv.threshold(B_imgajst,Bpos_thersh,255,cv.THRESH_BINARY)
        ret2, G_BiThresh = cv.threshold(G_imgajst,Gpos_thersh,255,cv.THRESH_BINARY)

        #print(B_BiThresh)
        #B_BiThresh_n = np.clip(B_BiThresh, 0, 255)
        B_contours, B_hierarchy = cv.findContours(B_BiThresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        imgB_info = "detected BCell = " + str(len(B_contours))

        G_contours, G_hierarchy = cv.findContours(G_BiThresh,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        imgG_info = "detected GCell = " + str(len(G_contours))

        #cv.rectangle(B_BiThresh,(10,15),(300,50),(255,255,255),thickness=2)
        BlblPts = np.array([[10,15],[10,50],[280,50],[280,15]],dtype=np.int32)
        cv.fillPoly(B_BiThresh,[BlblPts],(0,0,0),8,0)
        cv.polylines(B_BiThresh,[BlblPts],True,(255,255,255),thickness=2)
        cv.putText(B_BiThresh,imgB_info,(20,40),cv.FONT_HERSHEY_TRIPLEX,0.65,(255,255,255))  

        GlblPts = np.array([[10,15],[10,50],[280,50],[280,15]],dtype=np.int32)
        cv.fillPoly(G_BiThresh,[GlblPts],(0,0,0),8,0)
        cv.polylines(G_BiThresh,[GlblPts],True,(255,255,255),thickness=2)
        cv.putText(G_BiThresh,imgG_info,(20,40),cv.FONT_HERSHEY_TRIPLEX,0.65,(255,255,255))

        cv.imshow("Channel_Green_ROI",G_BiThresh) #gennerated window title with image selected
        cv.imshow("Channel_Blue_ROI",B_BiThresh) 
        
        #establish termination underneath
        c = cv.waitKey(1)
        if c==27:
            print("termination detected")
            #print(Bpos_ctrst)
            cv.destroyAllWindows()
            break
            
    

if __name__ == "__main__":
    img_adjustment()

