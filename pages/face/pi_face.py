from imutils.video import VideoStream
from imutils.video import FPS
from cv2 import cv2
import face_recognition
import argparse
import imutils
import pickle
import time
import os

def process():
	print("[INFO] loading encodings + face detector...")
	abs=os.path.abspath("pages")
	data = pickle.loads(open(str(abs)+"//face/encodings.pickle", "rb").read())
	detector = cv2.CascadeClassifier(str(abs)+"//face/haarcascade_frontalface_default.xml")

	frame = cv2.imread('./sawa/static/image.jpg')
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	boxes = [(int(y), int(x + w), (int)(y + h), int(x)) for (x, y, w, h) in rects]

	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	for encoding in encodings:
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		if True in matches:
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			name = max(counts, key=counts.get)
		
		names.append(name)
	
	for ((top, right, bottom, left), name) in zip(boxes, names):
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

	cv2.imwrite('./sawa/static/image.jpg', frame) 
	return names
	#cv2.imshow("Frame", frame)
	#cv2.waitKey(0)
	