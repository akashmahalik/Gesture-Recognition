import cv2
import os
import numpy as np 
import extract

e= extract.main()
print(e)
a0 = e[0][0]
a1 = e[0][1]
b0 = e[1][0]
b1 = e[1][1]
c0 = e[2][0]
c1 = e[2][1]
cv2.destroyAllWindows()
rgb=np.zeros((100,512,3),np.uint8)


lower_range=np.zeros((100,512,3),np.uint8)

upper_range=np.zeros((100,512,3),np.uint8)
draw = np.zeros((480,640,3), np.uint8)

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


oldcentr=(0,0)

while( cap.isOpened() ) :
	_,frame = cap.read()
	_,frame2 = cap.read()
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
	bgr1=cv2.cvtColor(np.uint8([[[0,30,103]]]),cv2.COLOR_HSV2BGR)
	bgr2=cv2.cvtColor(np.uint8([[[179,96,169]]]),cv2.COLOR_HSV2BGR)

	h=hsv.item(0,0,0)
	s=hsv.item(0,0,1)
	v=hsv.item(0,0,2)

	rgb[:]=[b,g,r]
	z=cv2.waitKey(1) & 0xFF
	if z == ord('y'):
		print(h,s,v)

	x=bgr1.item(0,0,0)
	y=bgr1.item(0,0,1)
	z=bgr1.item(0,0,2)
	
	
	lower_range[:]=[x,y,z]

	x=bgr2.item(0,0,0)
	y=bgr2.item(0,0,1)
	z=bgr2.item(0,0,2)
	
	upper_range[:]=[x,y,z]

	overlay=draw.copy()
	opacity=0.2
	cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	lower=np.array([a0,b0,c0])
	upper=np.array([a1,b1,c1])

	mask=cv2.inRange(hsv,lower,upper)

	res=cv2.bitwise_and(frame,frame,mask=mask)

	img_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	
	blur = cv2.GaussianBlur(mask,(5,5),0)
	#b=cv2.Canny(blur,200,450)
	ret,thresh = cv2.threshold(blur,255,255,cv2.THRESH_OTSU)
	thresh1=thresh.copy()
	
	a=cv2.Canny(thresh1,200,300)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
	a=cv2.Canny(thresh,200,300)
	max_area=0
	
	for i in range(len(contours)):
		cnt=contours[i]
		area = cv2.contourArea(cnt)
		if(area>max_area):
			max_area=area
			ci=i
	cnt=contours[ci]

	hull = cv2.convexHull(cnt)

	drawing = np.zeros(frame.shape,np.uint8)
	moments = cv2.moments(cnt)
	if moments['m00']!=0:
				cx = int(moments['m10']/moments['m00']) 
				cy = int(moments['m01']/moments['m00']) 

	centr=(cx,cy)
	dy=centr[1]-oldcentr[1]
	oldcentr=centr
	if dy<0:
		os.system("amixer -c 1 set Master 3%+")
	if dy>0:
		os.system("amixer -c 1 set Master 3%-")	
		

	cv2.circle(frame,centr,5,[0,0,255],2)
	cv2.circle(draw,centr,5,[0,255,0],-1)
	
	cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
	cv2.drawContours(drawing,[hull],0,(0,0,255),2)

	cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	hull = cv2.convexHull(cnt,returnPoints = False)


	if(1):
			defects = cv2.convexityDefects(cnt,hull)
			mind=0
			maxd=0
			for i in range(defects.shape[0]):
					s,e,f,d = defects[i,0]
					start = tuple(cnt[s][0])
					end = tuple(cnt[e][0])
					far = tuple(cnt[f][0])
					dist = cv2.pointPolygonTest(cnt,centr,True)
					cv2.line(frame,start,end,[0,255,0],2)

					cv2.circle(frame,far,5,[0,0,255],-1)
					
					i=0	


			
	cv2.imshow('fii',drawing)
	cv2.imshow('img',a)
	
	cv2.imshow('control & lower_range',rgb)
	cv2.imshow('lower_range_colour',lower_range)
	cv2.imshow('upper_range_colour',upper_range)
	cv2.imshow('frame',frame)
	cv2.imshow('final',res)
	cv2.imshow('mask',mask)
	cv2.imshow('draw',draw)
	
	
	k=cv2.waitKey(2) & 0xFF
	if k == ord('q'):
		break    

cv2.destroyAllWindows()
