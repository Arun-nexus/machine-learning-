import math
import cv2

img = cv2.VideoCapture(0)
flag=False
ex,ey,ix,iy=-1,-1,-1,-1
rectangle=[]
distance_points=[]
length=float(input("size of the pixel for conversion"))
calibrated=None
multi_tracker=cv2.legacy.MultiTracker_create()

def trackers(event,x,y,flags,params):
    global flag,ex,ey,ix,iy,rectangle,multi_tracker

    if event == cv2.EVENT_LBUTTONDOWN:
        flag=True
        ex,ey=x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flag:
            temp=frame.copy()
            cv2.rectangle(temp,(ex,ey),(x,y),(0,0,255),1)
            cv2.imshow("window",temp)
    elif event == cv2.EVENT_LBUTTONUP:
        flag=False
        ix,iy=x,y
        cv2.rectangle(frame,(ex,ey),(ix,iy),(0,0,255),1)
        rectangle.append((ex,ey,ix,iy))
        cv2.imshow("window", frame)
        xi,yi=min(ex,ix),min(iy,ey)
        w,h=abs(ex-ix),abs(ey-iy)

        roi=(xi,yi,w,h)
        roi=tuple(map(int,roi))
        track=cv2.legacy.TrackerCSRT_create()
        multi_tracker.add(track,frame,roi)


cv2.namedWindow("window")
cv2.setMouseCallback("window",trackers)


while True:

    ret,frame=img.read()
    if not ret:
        break
    tempo = frame.copy()

    rat,boxes=multi_tracker.update(frame)
    if rat:
        for box in boxes:
            x,y,w,h=[int(v) for v in box]
            distance_points.append([(w//2),(h//2)])
            cv2.rectangle(frame,(x,y),(w+x,y+h),(0,0,255),1)
        cv2.imshow("window",frame)

    if len(distance_points) >= 2:
        first,second=distance_points[0],distance_points[1]
        pixel_dist_known = math.dist(first,second)
        pixels_per_cm = pixel_dist_known / length
        real_dist = pixel_dist_known / pixels_per_cm
        for i in range(2, len(distance_points), 2):
            if i + 1 < len(distance_points):
                p1, p2 = distance_points[i], distance_points[i + 1]
                dist_cm = math.dist(p1, p2) / pixels_per_cm
                print(f"{dist_cm} cm")


    if cv2.waitKey(1) & 0xFF==ord("x"):
        break

img.release()
cv2.destroyAllWindows()