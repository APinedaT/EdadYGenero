#Inicializando Variables 
import argparse
import os
import numpy as np
import datetime
from centroidtracker import CentroidTracker
import cv2
import getmac
import mysql.connector

try:
    from openvino.inference_engine import IECore
    import cv2 as cv
except:
    raise Exception("""Inicializar variables OpenVino primero""")
# Estableciendo tiempo maximo y distancia para eliminar el ID
tracker = CentroidTracker(maxDisappeared=50, maxDistance=90)
#se obtiene la direccion mac del equipo
mac=getmac.get_mac_address()
print("Direccion MAC:",mac)

#Conexion a la base de datos 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="electronika"
)
#Agumentos que puede ser usados en la linea de comandos por consola en caso de querer cambiar el tipo de dispositivo o la entrada de video 
#tambien se pueden cambiar los default para otro tipo de dispositivo  o se puede cambiar la camara, en este caso es 0 ya que normalmente es una sola camara 
#en caso de tener mas mirar la posicion en el administrador de dispositvios y cambiarlo ejmp: default=1
parser = argparse.ArgumentParser(description="OpenVINO Face Detection")
parser.add_argument("-d", "--device", metavar='', default='CPU',
                    help="Device to run inference: GPU, CPU or MYRIAD", type=str)
parser.add_argument("-c", "--camera", metavar='', default=0,
                    help="Camera Device, default 0 for Webcam", type=int)
args = parser.parse_args()

device = args.device.upper()
plugin = IECore()
#Ubicacion de los modelos 
FACEDETECT_XML = "models/face-detection-adas-0001.xml"
FACEDETECT_BIN = "models/face-detection-adas-0001.bin"
model_age="models/age-gender-recognition-retail-0013.xml"
model_emotion="models/emotions-recognition-retail-0003.xml"
#padding para las cajas de las caras que se muestran
padding=20
#leyendo el modelo y creadn oel ejecutable del modelo de edad y genero 
net2 = plugin.read_network(model_age, os.path.splitext(model_age)[0] + ".bin")
exec_net2 = plugin.load_network(network=net2, num_requests=2, device_name=args.device)


#variables para la lista de personas
object_id_list = []
dtime = dict()
dwell_time = dict()
genero = dict()
edad = dict()

#procesamiento de la imagen para que el modelo la pueda leer 
def image_preprocessing(image, n, c, h, w):
    blob = cv.resize(image, (w, h))  
    blob = blob.transpose((2, 0, 1)) 
    blob = blob.reshape((n, c, h, w))
    return blob

#cargando el modelo de detecion de caras 
def load_model(plugin, model, weights, device):
    net = plugin.read_network(model, weights)
    exec_net = plugin.load_network(network=net, device_name=device)
    return net, exec_net

net_facedetect, exec_facedetect = load_model(plugin, FACEDETECT_XML, FACEDETECT_BIN, device)

#obteniendo inforamcion de los requerimientos de los modelos, en que formarmato y tamaño necesita el modelo las imaganes 
FACEDETECT_INPUTKEYS = 'data'
FACEDETECT_OUTPUTKEYS = 'detection_out'
n_facedetect, c_facedetect, h_facedetect, w_facedetect = net_facedetect.input_info[FACEDETECT_INPUTKEYS].input_data.shape
n_facedetect2, c_facedetect2, h_facedetect2, w_facedetect2 = exec_net2.input_info[FACEDETECT_INPUTKEYS].input_data.shape

#leyendo el argumeto de la camara y tomando el video 
input_stream = args.camera
cap = cv2.VideoCapture(input_stream)

# ciclo que se ejecuta hasta que opriman q o se finalice el servicio 
while True:

    if cap:
        hasFrame, image = cap.read()
    if not hasFrame:
        break
    # procesando imagen para la deteccion de caras 
    blob = image_preprocessing(
        image, n_facedetect, c_facedetect, h_facedetect, w_facedetect)
    
    req_handle = exec_facedetect.start_async(request_id=0, inputs={FACEDETECT_INPUTKEYS: blob})
    
    status = req_handle.wait()
    res = req_handle.output_blobs[FACEDETECT_OUTPUTKEYS].buffer
    faceBoxes=[]
    for detection in res[0][0]:
        confidence = float(detection[2]) 
        # si la confianza de que es una cara es mayor al 90% crea las cajas de las caras que detecto este valor se puede cambiar segun los requerimientos          
        if confidence > 0.9:
            xmin = int(detection[3] * image.shape[1])
            ymin = int(detection[4] * image.shape[0])
            xmax = int(detection[5] * image.shape[1])
            ymax = int(detection[6] * image.shape[0])
            faceBoxes.append([xmin, ymin, xmax, ymax])

            cv.rectangle(image, (xmin, ymin), (xmax, ymax), (255,0,0))
    
    # se recorre la matriz de faceboxes 
    for faceBox in faceBoxes:
        face=image[max(0,faceBox[1]-padding):
                   min(faceBox[3]+padding,image.shape[0]-1),max(0,faceBox[0]-padding)
                   :min(faceBox[2]+padding, image.shape[1]-1)]
        #procesamiento de la cara para detectar la edad y el genero 
        blob2 = image_preprocessing(face, n_facedetect2, c_facedetect2, h_facedetect2, w_facedetect2)
        out=exec_net2.infer(inputs={FACEDETECT_INPUTKEYS: blob2})

        #se obtienen los valores 
        age = out['age_conv3']
        prob = out['prob']
        age = age[0][0][0][0] * 100
        label = ('Mujer', 'Hombre')
        gender = label[np.argmax(prob[0])]
        
        rects = faceBoxes
        if not faceBoxes:
            rects=[]
            #actualiza el valor de las caras en este caso el if nos dice que no hay caras por lo cual lo actualiza para que elimine los IDs 
            objects,ulti= tracker.update(rects)
            # si se obtiene un valor de que se elimino un ID lo almacena en la base de datos 
            if ulti !=None :
                #print("Ultimo id eliminado",ulti)
                time_end=int(dwell_time[ulti]) 
                gender_end=genero[ulti]
                age_end=str(edad[ulti])
                mycursor = mydb.cursor()
                sql = "INSERT INTO reco (Tiempo, Genero, Edad, Expresion) VALUES (%s, %s, %s, %s)"
                val = (time_end, gender_end, age_end)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "Record insertado")
                print("ID",object_id_list[ulti],"time", time_end,"Genero",gender_end,"Edad",age_end,"Expresion",emotion_end)
        #actualiza las caras que se detectaron para que les asigne un ID a cada una 
        objects,ulti = tracker.update(rects)
        # si se obtiene un valor de que se elimino un ID lo almacena en la base de datos 
        if ulti !=None :
                print("Ultimo id eliminado",ulti)
                time_end=int(dwell_time[ulti]) 
                gender_end=genero[ulti]
                age_end=str(edad[ulti])
                mycursor = mydb.cursor()
                sql = "INSERT INTO reco (Tiempo, Genero, Edad, Expresion) VALUES (%s, %s, %s, %s)"
                val = (time_end, gender_end, age_end)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "Record insertado")
                print("ID",object_id_list[ulti],"time", time_end,"Genero",gender_end,"Edad",age_end,"Expresion",emotion_end)
        #recorre la matriza con la posicion de las caras y con los IDs para almacenar los daros en cada ID
        for (objectId, bbox) in objects.items():
            x1, y1, x2, y2 = bbox
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            #almacena Edad y genero para el ID en el que este 
            if bbox == faceBox:       
                genero[objectId]=gender
                edad[objectId]=round(age, 2)
                emocion[objectId]=emotion
            # si el Id no estaba antes creado lo crea e inicializa el tiempo 
            if objectId not in object_id_list:
                object_id_list.append(objectId)
                dtime[objectId] = datetime.datetime.now()
                dwell_time[objectId] = 0
            #si estaba creado solo actualiza el timepo 
            else:
                curr_time = datetime.datetime.now()
                old_time = dtime[objectId]
                time_diff = curr_time - old_time
                dtime[objectId] = datetime.datetime.now()
                sec = time_diff.total_seconds()
                dwell_time[objectId] += sec
            # pone los datos(ID,tiempo,edad y genero) en cada cara para el video de salida 
            text = "{}|{}".format(objectId, int(dwell_time[objectId]))
            cv2.putText(image, text, (x1-35, y1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
            cv2.putText(image, f'{gender}, {int(age)}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2, cv2.LINE_AA)
    #muestra el el video de salida, se pueden comentariar esta lienas en caso de no querer que se muestre el video 
    cv.namedWindow('Electronika Edad y genero', cv.WINDOW_NORMAL)
    cv.imshow('Electronika Edad y genero', image)
    key = cv2.waitKey(1)
    # si se oprime q en el cuadro de video se finaliza la aplicacion 
    if key == ord('q'):
        '''print("Object ID List",object_id_list)
        i=0
        while i<len(object_id_list):
            time_end=int(dwell_time[i]) 
            gender_end=genero[i]
            age_end=edad[i]
            print("ID",object_id_list[i],"time", time_end,"Genero",gender_end,"Edad",int(age_end))
            i+=1'''
        # obtiene el ultimo ID ya que este no ha sido eliminado y lo almacena en la base de datos 
        x=len(object_id_list)-1
        time_end=int(dwell_time[x]) 
        gender_end=genero[x]
        age_end=str(edad[x])
        mycursor = mydb.cursor()
        sql = "INSERT INTO reco (Tiempo, Genero, Edad, Expresion) VALUES (%s, %s, %s, %s)"
        val = (time_end, gender_end, age_end)
        mycursor.execute(sql, val)
        mydb.commit()
        print("ID",object_id_list[x],"time", time_end,"Genero",gender_end,"Edad",age_end,"Expresion",emotion_end)
        print(mycursor.rowcount, "Record insertado")
        break
cv2.destroyAllWindows()
