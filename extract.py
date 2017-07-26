import cv2
import numpy as np 
import sys

rgb=np.zeros((100,512,3),np.uint8)

lower_range=np.zeros((100,512,3),np.uint8)

upper_range=np.zeros((100,512,3),np.uint8)

cap=cv2.VideoCapture(0)


def nothing(x):
	pass 
cv2.namedWindow('control & lower_range')

cv2.createTrackbar('r','control & lower_range',0,255,nothing)
cv2.createTrackbar('g','control & lower_range',0,255,nothing)
cv2.createTrackbar('b','control & lower_range',0,255,nothing)

cv2.createTrackbar('lower_h','control & lower_range',0,180,nothing)
cv2.createTrackbar('upper_h','control & lower_range',0,180,nothing)
cv2.createTrackbar('lower_s','control & lower_range',0,255,nothing)
cv2.createTrackbar('upper_s','control & lower_range',0,255,nothing)
cv2.createTrackbar('lower_v','control & lower_range',0,255,nothing)
cv2.createTrackbar('upper_v','control & lower_range',0,255,nothing)




def main():
	while(1):
		_,frame = cap.read()
		r=cv2.getTrackbarPos('r','control & lower_range')
		g=cv2.getTrackbarPos('g','control & lower_range')
		b=cv2.getTrackbarPos('b','control & lower_range')

		lower_h=cv2.getTrackbarPos('lower_h','control & lower_range')
		upper_h=cv2.getTrackbarPos('upper_h','control & lower_range')
		lower_s=cv2.getTrackbarPos('lower_s','control & lower_range')
		upper_s=cv2.getTrackbarPos('upper_s','control & lower_range')
		lower_v=cv2.getTrackbarPos('lower_v','control & lower_range')
		upper_v=cv2.getTrackbarPos('upper_v','control & lower_range')
	
		hsv=cv2.cvtColor(np.uint8([[[b,g,r]]]),cv2.COLOR_BGR2HSV)
		bgr1=cv2.cvtColor(np.uint8([[[lower_h,lower_s,lower_v]]]),cv2.COLOR_HSV2BGR)
		bgr2=cv2.cvtColor(np.uint8([[[upper_h,upper_s,upper_v]]]),cv2.COLOR_HSV2BGR)

		h=hsv.item(0,0,0)
		s=hsv.item(0,0,1)
		v=hsv.item(0,0,2)

		rgb[:]=[b,g,r]
		z=cv2.waitKey(1) & 0xFF
		if z == ord('y'):
			print(lower_h,lower_s,lower_v)

		x=bgr1.item(0,0,0)
		y=bgr1.item(0,0,1)
		z=bgr1.item(0,0,2)
	
	
		lower_range[:]=[x,y,z]

		x=bgr2.item(0,0,0)
		y=bgr2.item(0,0,1)
		z=bgr2.item(0,0,2)
	
		upper_range[:]=[x,y,z]
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
		lower=np.array([lower_h,lower_s,lower_v])
		upper=np.array([upper_h,upper_s,upper_v])

		mask=cv2.inRange(hsv,lower,upper)

		res=cv2.bitwise_and(frame,frame,mask)
		cv2.imshow('control & lower_range',rgb)
		cv2.imshow('lower_range_colour',lower_range)
		cv2.imshow('upper_range_colour',upper_range)
		cv2.imshow('frame',frame)
		cv2.imshow('final',res)
		cv2.imshow('mask',mask)
	
	
		k=cv2.waitKey(2) & 0xFF
		if k == ord('q'):
			cap.release()
			break
	hsv = [[lower_h,upper_h],[lower_s,upper_s],[lower_v,upper_v]];    
	return hsv
	cv2.destroyAllWindows()
		

if __name__ == "__main__":
    main()



