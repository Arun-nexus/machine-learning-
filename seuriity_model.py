import cv2
import numpy as np
import winsound
img =cv2.VideoCapture(0)

rectangle_flag=False
ex,ey,ix,iy=-1,-1,-1,-1
frame = None
rectangles =  []
prev_roi={}
flags={}
def security(event,x,y,flags,param):
    global rectangle_flag,ex,ey,ix,iy,frame

    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle_flag = True
        ex,ey=x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle_flag:
            temp=frame.copy()
            cv2.rectangle(temp,(ex,ey),(x,y),(0,0,255),1)
            cv2.imshow("window",temp)
    elif event == cv2.EVENT_LBUTTONUP:
        rectangle_flag = False
        ix,iy=x,y
        rectangles.append(((ex,ey),(ix,iy)))

        cv2.rectangle(frame, (ex, ey), (ix, iy), (0, 0, 255), 1)

cv2.namedWindow("window")
cv2.setMouseCallback("window",security)


while True:

    rat,frame = img.read()

    if not rat:
        break

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    for idx, r in enumerate(rectangles):

        (x1,y1),(x2,y2)=r
        x1,x2=min(x1,x2),max(x1,x2)
        y1,y2=min(y1,y2),max(y1,y2)

        roi = gray[y1:y2,x1:x2]

        if roi.size>0:
            if idx not in prev_roi:
                prev_roi[idx] = roi.copy()
            else:
                if prev_roi[idx].shape == roi.shape:
                    diff=np.mean(cv2.absdiff(prev_roi[idx],roi))
                    if diff > 50:
                        flags[idx]=True
                    else:
                        flags[idx]=False

                if flags[idx]:
                    print("unaurthorized object detected")
                    winsound.Beep(1000,300)
        cv2.rectangle(frame,r[0],r[1],(0,0,255))


    cv2.imshow("window",frame)



    if cv2.waitKey(1) & 0xFF == ord("x"):
        break
img.release()
cv2.destroyAllWindows()
