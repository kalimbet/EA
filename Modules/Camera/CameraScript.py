import cv2
import numpy as np
import sqlite3
import os
import json
import datetime

def load_and_save(user_dic):
  try:
    data = json.load(open('cashe_file.json'))
  except:
    data = []
  data.append(user_dic)

  with open("cashe_file.json", "w") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

def get_user(name,date,time):
  user = {
    "id": ids,
    "name": name,
    "Room id": 1,
    "Date": str(date),
    "Time": str(time),
  }
  return user

conn = sqlite3.connect('Database/database.db')
c = conn.cursor()
fname = "recognizer/trainingData.yml"
if not os.path.isfile(fname):
  print("Please train the data first")
  exit(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(fname)
while True:
  ret, img = cap.read()
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
    ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
    c.execute("select name from users where id = (?);", (ids,))
    result = c.fetchall()
    name = result[0][0]
    dateT = datetime.datetime.now().date()
    timeT = datetime.datetime.now().time()
    if conf < 50:
      cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
      load_and_save(get_user(name,dateT,timeT))
    else:
      cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
  cv2.imshow('Face Recognizer',img)
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break
cap.release()
cv2.destroyAllWindows()



