import cv2
cap=cv2.VideoCapture(0)
tracking=False
ix,iy,ex,ey=-1,-1,-1,-1
frame=None

rectangles=[]
multi_tracker=cv2.legacy.MultiTracker_create()

def tracker(event,x,y,flags,params):
    global tracking,ix,iy,ex,ey,frame,multi_tracker
    if event == cv2.EVENT_LBUTTONDOWN:
        tracking=True
        ix,iy=x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if tracking :
            temp=frame.copy()
            cv2.rectangle(temp,(ix,iy),(x,y),(0,0,155),2)
            cv2.imshow("window",temp)
    elif event == cv2.EVENT_LBUTTONUP:
        tracking=False
        ex,ey=x,y
        cv2.rectangle(frame,(ix,iy),(x,y),(0,0,155),2)
        x0,y0=min(ix,ex),min(iy,ey)
        w,h=abs(ex-ix),abs(ey-iy)
        roi = (int(x0),int(y0),int(w),int(h))

        track = cv2.legacy.TrackerCSRT_create()
        multi_tracker.add(track,frame,roi)
        rectangles.append([ix,iy,ex,ey])


cv2.namedWindow("window")
cv2.setMouseCallback("window",tracker)

while True:
    rat, frame = cap.read()
    if not rat:
        break

    success,boxes=multi_tracker.update(frame)

    if success:
        for box in boxes:
            x,y,w,h=[int(v) for v in box]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,155),2)
        cv2.imshow("window",frame)

    cv2.imshow("window",frame)

    if cv2.waitKey(1) & 0xFF==ord("x"):

        break
cap.release()
cv2.destroyAllWindows()
