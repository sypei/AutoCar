import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier('src/cascades/data/                                                 haarcascade_frontalface_alt2.xml')
body_cascade = cv2.CascadeClassifier('src/cascades/data/haarcascade_fullbody.xml')
traffic_light_cascade = cv2.CascadeClassifier('src/cascades/data/haarcascade_trafficlight.xml')
speed_limit_cascade = cv2.CascadeClassifier('src/cascades/data/haarcascade_speedlimit.xml')
stop_sign_cascade = cv2.CascadeClassifier('src/cascades/data/haarcascade_stopsign.xml')

"""
boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]
"""
lower_red = np.array([17,15,100])
upper_red = np.array([50,56,200])
lower_yellow = np.array([17,80,100])
upper_yellow = np.array([100,200,200])
lower_green = np.array([17,100,15])
upper_green = np.array([50,200,56])


def detect_face(frame):	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	if len(faces)!=0:
		return True
	else:
		return False

def detect_body(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)
	
	if len(bodies)!=0:
		return True
	else:
		return False
		
def detect_speed_limit(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	speedlimits = speedlimit_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)
	
	if len(speedlimits)!=0:
		return True
	else:
		return False
		
def detect_stop_sign(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	stopsigns = stopsign_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)
	
	if len(stopsigns)!=0:
		return True
	else:
		return False		


def detect_traffic_light(frame):
	count_red = 0
	count_yellow = 0
	count_green = 0
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	lights = body_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)
	if len(lights)!=0:
		for(x,y,w,h) in lights:
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			hsv = cv2.cvtColor(roi_color, cv2.COLOR_BGR2HSV)
			for i in range(h):
				for j in range(w):
					if hsv[y+j,x+i]>lower_red and hsvhsv[y+j,x+i]<upper_red:
						count_red+=1
					elif hsv[y+j,x+i]>lower_yellow and hsvhsv[y+j,x+i]<upper_yellow:
						count_yellow+=1
					elif hsv[y+j,x+i]>lower_green and hsvhsv[y+j,x+i]<upper_green:
						count_green+=1
					else:
						pass
			max_count = max(count_green,count_red,count_yellow)
			if max_count == count_green:
				light_color = 'green'
			elif max_count == count_red:
				light_color = 'red'
			elif max_count ==count_yellow:
				light_color = 'yellow'
	else:
		light_color = 'none'
				
	return light_color
				

				    
				    
			
		    
		
		
	

	
		
	


	
	

