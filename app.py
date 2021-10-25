#A Gender and Age Detection program by Mahesh Sawant

import cv2
import math
import argparse
import datetime
import ctypes
from centroidtracker import CentroidTracker
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="electronika"
)

tracker = CentroidTracker(maxDisappeared=40, maxDistance=90)

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes


parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()

faceProto="opencv_face_detector.pbtxt"
faceModel="opencv_face_detector_uint8.pb"
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"
genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Hombre','Mujer']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

video=cv2.VideoCapture(args.image if args.image else 0)
padding=20

object_id_list = []
dtime = dict()
dwell_time = dict()
genero = dict()
edad = dict()
rects=[]
while True:
    hasFrame,frame=video.read()
    
    resultImg,faceBoxes=highlightFace(faceNet,frame)
    
    if not faceBoxes:
        rects=[]
        #print(rects)
        objects,ulti= tracker.update(rects)
        if ulti !=None :
            print("Ultimo id eliminado",ulti)
            time_end=int(dwell_time[ulti]) 
            gender_end=genero[ulti]
            age_end=edad[ulti]
            mycursor = mydb.cursor()
            sql = "INSERT INTO reco (Tiempo, Genero, Edad) VALUES (%s, %s, %s)"
            val = (time_end, gender_end, age_end)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Record insertado")
            print("ID",object_id_list[ulti],"time", time_end,"Genero",gender_end,"Edad",age_end)


    
    for faceBox in faceBoxes:
        
        face=frame[max(0,faceBox[1]-padding):
                   min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                   :min(faceBox[2]+padding, frame.shape[1]-1)]
        #print(faceBox[0],faceBox[1])

                   
        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]
        #print(f'Gender: {gender}')
        
        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        #print(f'Age: {age[1:-1]} years', "ID",objectId)

        rects = faceBoxes
        objects,ulti = tracker.update(rects)
        if ulti != None:
            #print("Ultimo id eliminado",ulti)
            time_end=int(dwell_time[ulti]) 
            gender_end=genero[ulti]
            age_end=edad[ulti]
            mycursor = mydb.cursor()
            sql = "INSERT INTO reco (Tiempo, Genero, Edad) VALUES (%s, %s, %s)"
            val = (time_end, gender_end, age_end)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "Record insertado")
            print("ID",object_id_list[ulti],"time", time_end,"Genero",gender_end,"Edad",age_end)
        for (objectId, bbox) in objects.items():
            x1, y1, x2, y2 = bbox

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            #print("largo",len(faceBoxes))
            #print("toda la matriz",faceBoxes)
            #print("el index que busca",objectId)
            #print(faceBox,faceBoxes[objectId])
            #i=0
            #while i<len(faceBoxes):
                #print(bbox)
                #print(faceBox)
                #print("i",i)
            if bbox == faceBox:
                #if faceBox == faceBoxes[i]:
                    #print("puede funcionar por aca")
                    #print(faceBox,faceBoxes[objectId])
                    #if objectId not in object_id_list:
                
                genero[objectId]=gender
                edad[objectId]=age
                #elif faceBox != faceBoxes[i]:
                    #print("no es igual")
                #i+=1
            
            
            if objectId not in object_id_list:
                object_id_list.append(objectId)
                #print("ID",objectId,"Genero",genero[objectId],"Edad",edad[objectId])
                dtime[objectId] = datetime.datetime.now()
                dwell_time[objectId] = 0
            else:
                curr_time = datetime.datetime.now()
                old_time = dtime[objectId]
                time_diff = curr_time - old_time
                dtime[objectId] = datetime.datetime.now()
                sec = time_diff.total_seconds()
                dwell_time[objectId] += sec
            
            #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            text = "{}|{}".format(objectId, int(dwell_time[objectId]))
            cv2.putText(resultImg, text, (x1-35, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
        #print("salio del for",)
        #print(len(object_id_list),"IDs",object_id_list)
        #print(faceBox,"position1",faceBoxes[1])
    cv2.imshow("Detecting age and gender", resultImg)
    notepad_handle = ctypes.windll.user32.FindWindowW(None, "Untitled - Notepad")
    #notepad_handle = ctypes.windll.user32.FindWindowW(u"Detecting age and gender", None) 
    ctypes.windll.user32.ShowWindow(notepad_handle, 6)
    #print("Salio del for2")
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("Aquii")
        print("Object ID List",object_id_list)
        i=0
        while i<len(object_id_list):
            time_end=int(dwell_time[i]) 
            gender_end=genero[i]
            age_end=edad[i]
            print("ID",object_id_list[i],"time", time_end,"Genero",gender_end,"Edad",age_end)
            i+=1

        x=len(object_id_list)-1
        time_end=int(dwell_time[x]) 
        gender_end=genero[x]
        age_end=edad[x]
        mycursor = mydb.cursor()
        sql = "INSERT INTO reco (Tiempo, Genero, Edad) VALUES (%s, %s, %s)"
        val = (time_end, gender_end, age_end)
        mycursor.execute(sql, val)
        mydb.commit()
        print("ID",object_id_list[x],"time", time_end,"Genero",gender_end,"Edad",age_end)
        print(mycursor.rowcount, "Record insertado")
        break
cv2.destroyAllWindows()
