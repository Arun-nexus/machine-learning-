import csv

import torch.nn
from torchvision import  models,transforms
from PIL import Image
import json

file_path = r"C:\Users\Arun\Downloads\translation.json"

with open(file_path, 'r') as f:
  translation_data = json.load(f)
  dictionary=translation_data

num_classes = 151

model=models.vgg19(weights = None)
model.classifier[6]=torch.nn.Linear(4096,num_classes)
state_dict=torch.load(r"C:\Users\Arun\Downloads\animal_cnn_vgg19 (1).pth")

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor()
])


import cv2

cam = cv2.VideoCapture(0)
ractangle=False
frame = None
rectangle=[]
ex,ey,ix,iy=-1,-1,-1,-1
def crop(event,x,y,flag,param):
    global ractangle,ex,ey,ix,iy,rectangle,frame
    if event == cv2.EVENT_LBUTTONDOWN:
        ractangle = True
        ex,ey=x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        temp = frame.copy()
        cv2.rectangle(temp,(ex,ey),(x,y),(0,0,255),1)

    elif event == cv2.EVENT_LBUTTONUP:
        ractangle = False
        ix,iy=x,y
        cv2.rectangle(frame,(ex,ey),(ix,iy),(0,0,255),1)
        rectangle.append([ex,ey,ix,iy])

        for i in rectangle:
            if i[2] > -1 and i[3] > -1:
                cropped_image = frame[min(i[1], i[3]):max(i[1], i[3]), min(i[0], i[2]):max(i[0], i[2])]
                img = cv2.cvtColor(cropped_image,cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = transform(img).unsqueeze(0)

                with torch.no_grad():
                    output = model(img)
                    _,pred = torch.max(output,1)
                    pred = pred.item()
                for j in dictionary:
                    if j == pred:
                        predicted = dictionary[j]
                        cv2.putText(cropped_image,f"{predicted}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1)
                cv2.imshow(f"rectangle{i}", mat=cropped_image)
cv2.namedWindow("window")
cv2.setMouseCallback("window",crop)


while True:

    ret,frame = cam.read()
    if not ret:
        break
    cv2.imshow("window",frame)

    if cv2.waitKey(1) & 0xFF == ord("x"):
        break

cam.release()
cv2.destroyAllWindows()